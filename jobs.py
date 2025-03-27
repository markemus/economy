import copy
import math
import random

import database as d
from conversation import Convo


# not all jobs, but all jobs you can create (not manager, priest)
def all_jobs():
    job_list = [Baker, Brewer, Carrier, Farmer, Miller, Lumberjack, Carpenter]
    return job_list


class Job(object):
    jobType = "Generic_job"
    jobVerb = "Genericking"
    naturalWage = 0

    def __init__(self, slots, business, unit, salary):
        # slots is an int, number of employee slots available
        equipLength = len(d.getEquipment())
        self.slots = slots
        self.business = business
        self.unit = unit
        self.equipment = [0 for equip in range(equipLength)]
        self.employees = []
        self.salary = salary
        self.business.addJob(self)
        self.unit.addJob(self)
        self.locality = self.unit.getLocality()
        self.idlers = []

    @property
    def name(self):
        return self.jobType

    def getBusiness(self):
        return self.business

    def getEquipment(self):
        return self.equipment

    def getSalary(self):
        return self.salary

    def getSlots(self):
        return self.slots

    def getUnit(self):
        return self.unit

    def getJobType(self):
        return self.jobType

    def incrementSlots(self):
        self.slots += 1

    def decrementSlots(self):
        self.slots -= 1

    def setSlots(self, slots):
        self.slots = slots

    def getEmployees(self):
        return self.employees

    def get_emp_dict(self):
        empDict = {}
        empDict[self] = copy.copy(self.employees)
            
        return empDict

    def takeIdlers(self, amount):
        if amount != 0:
            workers = self.idlers[-amount:]
            self.idlers = self.idlers[:-amount]
        else:
            workers = []

        return workers

    def resetIdlers(self):
        self.idlers = copy.copy(self.employees)

    def craft(self, productIndex, amount):
        components = d.getComponents(productIndex)
        tech = self.unit.getTech(productIndex)
        DMClist = self.unit.getDMC()
        productDMC = 0

        # reduce to components
        for component in components:
            materialIndex = component[0]
            inStock = self.unit.getStock(materialIndex)
            ratio = component[1]
            enoughFor = inStock / ratio

            if amount > (enoughFor):
                amount = enoughFor

            # DMC
            componentDMC = DMClist[materialIndex]
            productDMC += componentDMC * ratio

        # reduce to available employees
        capability = (len(self.idlers) * tech)
        if amount > capability:
            amount = capability

        # take employees from idlers (so they can't do anything else today)
        working = math.ceil(amount / tech)
        workers = self.takeIdlers(working)

        # take components
        for component in components:
            materialIndex = component[0]
            ratio = component[1]
            used = amount * ratio
            self.unit.addStock(materialIndex, -used)

        # add product- goes to stock for assembly lines. Crafted is for natural price calculation.
        self.unit.addCrafted(productIndex, amount)
        self.unit.addStock(productIndex, amount)

        # set product DMC
        self.unit.setDMC(productIndex, productDMC)

        for craftsman in workers:
            craftsman.think("We crafted " + str(amount) + " " + d.getMaterials()[productIndex] + " today.")
    
    def plant(self, productIndex, amount):
        product = d.getMaterials()[productIndex]

        if d.isInSeason(productIndex, self.business.model.calendar.state):
            components = d.getComponents(productIndex)
            tech = self.unit.getTech(productIndex)
            growing = self.unit.growingPlants(productIndex)
            DMClist = self.unit.getDMC()
            isEnough = True
            productDMC = 0

            # subtract already growing
            if amount > growing:
                amount = amount - growing
                isAllPlanted = False
            else:
                amount = 0
                isAllPlanted = True

            # plant
            if not isAllPlanted:
                # reduce to components
                for component in components:
                    materialIndex = component[0]
                    inStock = self.unit.getStock(materialIndex)
                    ratio = component[1]
                    enoughFor = inStock / ratio

                    if amount > (enoughFor):
                        amount = enoughFor
                        isEnough = False

                    # DMC
                    componentDMC = DMClist[materialIndex]
                    productDMC += componentDMC * ratio

                # reduce to employees
                capability = (len(self.idlers) * tech)
                if amount > capability:
                    amount = capability

                # take employees from idlers (so they can't do anything else today)
                working = math.ceil(amount / tech)
                workers = self.takeIdlers(working)

                # take components
                for component in components:
                    materialIndex = component[0]
                    ratio = component[1]
                    used = amount * ratio
                    self.unit.addStock(materialIndex, -used)

                # add product- goes to stock for assembly lines. Crafted is for natural price calculation.
                self.unit.plantSeeds(productIndex, amount)
                self.unit.addPlanted(productIndex, amount)

                # set product DMC
                self.unit.setDMC(productIndex, productDMC)

                for farmer in workers:
                    if not isEnough:
                        farmer.think("We ran out of materials for " + product + " at work today.")
                    farmer.think("We planted " + str(amount) + " " + product + " today.")
            else:
                for farmer in self.getEmployees():
                    farmer.think("We've already planted enough " + product + " for the season.")
        else:
            for farmer in self.getEmployees():
                farmer.think("It's not the planting season for " + product + ".")

    def harvest(self, productIndex):
        tech = self.unit.getTech(productIndex)
        product = d.getMaterials()[productIndex]
        
        amount = (len(self.idlers) * tech)        
        ripe = self.unit.ripePlants(productIndex)

        if amount > ripe:
            amount = ripe

        # take employees from idlers (so they can't do anything else today)
        working = math.ceil(amount / tech)
        workers = self.takeIdlers(working)

        self.unit.harvest(productIndex, amount)
        self.unit.addHarvested(productIndex, amount)

        for farmer in workers:
            farmer.think("We harvested " + str(amount) + " " + product + " today.")


class Baker(Job):
    jobType = "Baker"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addCraftingJob(self)


class Brewer(Job):
    jobType = "Brewer"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addCraftingJob(self)


class Carrier(Job):
    jobType = "Porter"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)

    # TODO allow transports from non-owned but known units. Currently no money is transferred.
    # takes from unit1 output[] and places in unit2 stock[] 
    def transportMats(self, unit1, unit2, materialIndex, amount):
        business1 = unit1.getBusiness()
        business2 = unit2.getBusiness()
        amountInStock = unit1.getStock(materialIndex)
        isTransport = False

        # transport
        if (business1 == self.business):
            if (business2 == self.business):
                if (amount > amountInStock):
                    unit1.addFailTransports(materialIndex, amount - amountInStock)
                    amount = amountInStock

                if amount > 0:
                    # DMC is the FULL natural price of the material, not just its DMC- it's the DMC of products MADE FROM this material.
                    # we want natural price because we don't care about supply and demand within businesses.
                    DMC = unit1.priceCalc(materialIndex)[2]
                    unit2.setDMC(materialIndex, DMC)
                    
                    unit1.addTransports(materialIndex, amount)
                    unit2.addPurchase(materialIndex, amount)

                    # transport
                    unit1.addStock(materialIndex, -amount)
                    unit2.addStock(materialIndex, amount)
                    
                    isTransport = True

        # thoughts
        for employee in self.getEmployees():
            if isTransport == True:
                employee.think("I carried " + str(amount) + " things today.")
            else:
                employee.think("My boss sent me on a wild goose chase today.")

        return isTransport


class Farmer(Job):
    jobType = "Farmer"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addCraftingJob(self)
        # self.business.addHarvestJob(self)


class Owner(Job):
    jobType = "Job Creator"

    def __init__(self, business, unit):
        Job.__init__(self, 1, business, unit, salary=6)


class Manager(Job):
    jobType = "Manager"

    def __init__(self, business, unit, salary):
        Job.__init__(self, 1, business, unit, salary)

    def transferMats(self, theUnit, materialIndex, amount):
        """Takes from theUnit stock[] and places in theUnit output[], filling output[] up to amount."""
        ourBusiness = self.getUnit().getBusiness()
        business = theUnit.getBusiness()
        isTransfer = False

        if len(self.employees) > 0:
            manager = self.employees[0]

            if amount > theUnit.getStock(materialIndex):
                amount = theUnit.getStock(materialIndex)
            if amount > theUnit.getOutput(materialIndex):
                amount -= theUnit.getOutput(materialIndex)
            else:
                amount = 0

            theUnit.addStock(materialIndex, -amount)
            theUnit.addOutput(materialIndex, amount)
            isTransfer = True

            # thoughts
            if isTransfer:
                if amount != 0:
                    manager.think("I transfered " + str(amount) + " " + d.materialsList[materialIndex] + " to " + theUnit.name + "'s output.")
                else:
                    manager.think("My employees didn't have the " + d.materialsList[materialIndex] + " ready when I needed it.")
            else:
                manager.think("I can't transfer goods at " + str(theUnit) + ". Strange...")

        else:
            amount = 0

        return amount

    def updatePrices(self, jobUnit):
        if jobUnit.business == self.business:
            jobUnit.priceGen()


class Miller(Job):
    jobType = "Miller"
    jobVerb = "Milling"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addCraftingJob(self)


class Lumberjack(Job):
    jobType = "Lumberjack"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addHarvestJob(self)


class Carpenter(Job):
    jobType = "Carpenter"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addCraftingJob(self)


# religious jobs
class Priest(Job):
    jobType = "Priest"

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)
        self.business.addPriestJob(self)

    def service(self):
        attendance = self.unit.getAttendance()
        approvedSongs = self.unit.getReligion().getSongs()
        song = random.choice(approvedSongs)

        # pray
        # TODO thoughts should have MU effect- religious needs, workout needs, socialization needs.
        #  Should have different messages depending how well it worked.
        for congregant in attendance:
            congregant.think("I love " + song + "!")
            congregant.think("The service at " + self.unit.name + " was beautiful.")
        # talk
        self.mingle()
        # go home
        self.unit.resetAttendance()

    def mingle(self):
        attendance = self.unit.getAttendance()
        for congregant in attendance:
            i = random.randrange(len(attendance))
            conversee = attendance[i]

            if conversee is not congregant:
                Convo.beginConversation(congregant, conversee)
