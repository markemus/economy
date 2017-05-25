import database as d
import random
import copy
from conversation import Convo

def all_jobs():
    job_list = [Baker, Brewer, Carrier, Farmer, Manager, Miller, Lumberjack, Carpenter, Priest]
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

    def craft(self, productIndex, amount):
        components =  d.getComponents(productIndex)
        tech = self.unit.getTech(productIndex)
        DMClist = self.unit.getDMC()
        productDMC = 0

        #reduce to components
        for component in components:
            materialIndex = component[0]
            inStock = self.unit.getStock(materialIndex)
            ratio = component[1]
            enoughFor = inStock / ratio

            if amount > (enoughFor):
                amount = enoughFor

            #DMC
            componentDMC = DMClist[materialIndex]
            productDMC += componentDMC * ratio

        #reduce to employees
        capability = (len(self.employees) * tech)
        if amount > capability:
            amount = capability

        #take components
        for component in components:
            materialIndex = component[0]
            ratio = component[1]
            used = amount * ratio
            self.unit.addStock(materialIndex, -used)

        #add product- goes to stock for assembly lines. Crafted is for natural price calculation.
        self.unit.addCrafted(productIndex, amount)
        self.unit.addStock(productIndex, amount)

        #set product DMC
        self.unit.setDMC(productIndex, productDMC)

        for craftsman in self.getEmployees():
            craftsman.think("I crafted " + str(amount) + " " + d.getMaterials()[productIndex] + " today.")

    #UNDER CONSTRUCTION
    #simple, for now
    def plant(self, materialIndex, amount):
        #seeds are pounds of seeds- ~14500 seeds per pound, for the record
        # jobUnit = self.getUnit()
        seedsPer = 50
        seeds = self.unit.getStock(materialIndex)
        growing = self.unit.growingPlants(materialIndex)
        farmers = len(self.getEmployees())
        isEnough = True
        isAllPlanted = False
        material = d.getMaterials()[materialIndex]

        #reduce to number of seeds we have
        if amount > seeds:
            amount = seeds

        #subtract already growing
        if amount > growing:
            amount = amount - growing
        else:
            amount = 0

        #limit by farmer ability
        maxPlanting = farmers * seedsPer
        if amount > maxPlanting:
            amount = maxPlanting

        #planting
        self.unit.plantSeeds(materialIndex, amount)

        #thoughts
        for farmer in self.getEmployees():
            if not isEnough:
                farmer.think("I ran out of " + material + " seeds at work today.")
            if isAllPlanted:
                farmer.think("I finished planting "+ material + " today.")
            farmer.think("I planted " + material + " seeds today.")

    def harvest(self, materialIndex, amount):
        tech = self.unit.getTech(materialIndex)
        material = d.getMaterials()[materialIndex]
        
        capability = (len(self.employees) * tech)
        ripe = self.unit.ripePlants(materialIndex)

        if amount > capability:
            amount = capability

        if amount > ripe:
            amount = ripe

        self.unit.harvest(materialIndex, amount)

        for farmer in self.getEmployees():
            farmer.think("I harvested " + str(amount) + " " + material + " today.")




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

    # takes from unit1 output[] and places in unit2 stock[] 
    def transportMats(self, unit1, unit2, materialIndex, amount):
        business1 = unit1.getBusiness()
        business2 = unit2.getBusiness()
        amountInStock = unit1.getOutput(materialIndex)
        isTransport = False

        #transport
        if (business1 == self.business):
            if (business2 == self.business):
                if (amount > amountInStock):
                    amount = amountInStock
                if amount > 0:
                    priceList = unit1.getPrice()
                    materialPrice = priceList[materialIndex]
                    unit1.addSales(materialIndex, amount)
                    unit2.setDMC(materialIndex, materialPrice)
                    unit2.addPurchase(materialIndex, amount)
                    unit1.addOutput(materialIndex, -amount)
                    unit2.addStock(materialIndex, amount)
                    isTransport = True

        #thoughts
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
        self.business.addHarvestJob(self)




class Manager(Job):

    jobType = "Manager"

    def __init__(self, business, unit, salary):
        Job.__init__(self, 1, business, unit, salary)

    # takes from theUnit stock[] and places in theUnit output[], filling outupt[] up to amount.
    def transferMats(self, theUnit, materialIndex, amount):
        ourBusiness = self.getUnit().getBusiness()
        business = theUnit.getBusiness()
        isTransfer = False

        if len(self.employees) > 0:
            manager = self.employees[0]

            if (business == ourBusiness):
                if (amount > theUnit.getStock(materialIndex)):
                    amount = theUnit.getStock(materialIndex)
                if amount > theUnit.getOutput(materialIndex):
                    amount -= theUnit.getOutput(materialIndex)

                theUnit.addStock(materialIndex, -amount)
                theUnit.addOutput(materialIndex, amount)
                isTransfer = True

            if isTransfer:
                if amount != 0:
                    manager.think("I transfered " + str(amount) + " " + d.materialsList[materialIndex] + " to " + theUnit.name + "'s output.")
                else:
                    manager.think("My employees didn't have the " + d.materialsList[materialIndex] + " ready when I needed it.")
            else:
                manager.think("Why am I being asked to transfer goods that don't belong to us?")

        return isTransfer

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






#religious jobs
class Priest(Job):

    jobType = 'Priest'

    def __init__(self, slots, business, unit, salary):
        Job.__init__(self, slots, business, unit, salary)

    def service(self):
        attendance = self.unit.getAttendance()
        approvedSongs = self.unit.getReligion().getSongs()
        song = random.choice(approvedSongs)

        #pray
        for congregant in attendance:
            congregant.think("I love " + song + "!")
            congregant.think("The service at " + self.unit.name + " was beautiful.")
        #talk
        self.mingle()
        #go home
        self.unit.resetAttendance()

    def mingle(self):
        attendance = self.unit.getAttendance()
        for congregant in attendance:
            i = random.randrange(len(attendance))
            conversee = attendance[i]

            if conversee is not congregant:
                Convo.beginConversation(congregant, conversee)