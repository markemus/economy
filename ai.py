import math
import random

import numpy as np

import business as bu
import database as d
import jobs
import people as p
import unit as u


# TODO review ai and see if we can improve it.
# singleton
class StartupAI(object):
    def __init__(self):
        None

    # O(n^2). Not ideal, but n SHOULD be low. Can we make O(n)?
    def whatToBuild(self, investor):
        # knownStock = self.knownStock(investor)
        # current dumb ai will build full product lines, so all are equally possible.
        # possibilities = self.possibilities(investor, knownStock)
        possibilities = self.tempPossibilities(investor)
        optimalList = self.optimalList(investor)
        bestPossible = self.weightedBestPossible(possibilities, optimalList)

        return bestPossible

    def knownStock(self, investor):
        requiredStock = d.getAllComponents()
        manuProfiles = investor.getKnownManus()
        knownStock = [False for i in requiredStock]

        for manu in manuProfiles:
            priceList = manu.getPrices()

            for i in range(len(priceList)):
                if priceList[i] != 0:
                    knownStock[i] = True

        return knownStock

    def tempPossibilities(self, investor):
        possibilities = [True for i in d.getMaterials()]

        for business in investor.getBusinesses():
            for order in business.getCraftOrders():
                possibilities[order.getProductIndex()] = False

        return possibilities

    # which products can the investor find stock for?
    # O(n^2)- not exactly, but multivariate
    def possibilities(self, investor, knownStock):
        requiredStock = d.getAllComponents()
        possibilities = [False for i in requiredStock]

        for i in range(len(requiredStock)):
            target = requiredStock[i]
            hasStock = True

            for componentRatio in target:
                component = componentRatio[0]
                if not knownStock[component]:
                    hasStock = False
            
            if hasStock:
                possibilities[i] = True

        return possibilities

    # people shop for the thing they want the most. So they want to open businesses with that in mind- what will bring in the most customers?
    def optimalList(self, investor):
        peopleProfiles = investor.getKnownPeople()
        # highestMU = [0 for i in d.getMaterials()]
        mu_lists = np.array([profile.getMuList()[0] for profile in peopleProfiles])
        mu_avg = mu_lists.mean(axis=0)
        mu_avg = mu_avg / mu_avg.sum()

        return mu_avg

    # TODO businesses should not build everything
    def weightedBestPossible(self, possibilities, optimalList):
        """Selects a good business to build, weighted on friends' marginal utility."""
        notDone = True

        while notDone:
            option = list(optimalList).index(np.random.choice(optimalList, p=optimalList))
            
            if optimalList[option] == 0:
                option = None
                notDone = False

            if option is not None:
                if possibilities[option]:
                    notDone = False
                else:
                    optimalList[option] = 0
                    if optimalList.sum() != 0:
                        optimalList = optimalList / optimalList.sum()
                    else:
                        notDone = False

        return option


# factory for supply chains.
class Builder(object):
    def __init__(self, model):
        self.model = model

    # TODO-DONE can we get rid of this fake initial_demand and let them learn entirely from failedSales?
    # def initial_demand(self, unit):
    #     for i in range(len(unit.can_make)):
    #         if unit.can_make[i]:
    #             unit.failSales[i] = 500

    # TODO-DONE jobs should be allowed per unit, you shouldn't be able to create any job in any unit.
    def jobMaker(self, unit):
        # unitJobLink = { "Farm"      : jobs.Farmer,
        #                 "Brewery"   : jobs.Brewer,
        #                 "Mill"      : jobs.Miller,
        #                 "Bakery"    : jobs.Baker,
        #                 "Lumberyard": jobs.Lumberjack,
        #                 "Joinery"   : jobs.Carpenter}
        # TODO slots should be more dynamic- it looks like currently units will always hire to max?
        slots = unit.getSlots()
        salary = 6
        new_jobs = []

        for job_type in unit.allowed_jobs:
            job_slots = slots // len(unit.allowed_jobs)
            new_job = job_type(job_slots, unit.getBusiness(), unit, salary)
            new_jobs.append(new_job)

        return new_jobs

    # also makes transfer orders
    def craftOrderMaker(self, job):
        jobProductLink = {"Farmer": [d.GRAIN_INDEX],
                          "Miller": [d.FLOUR_INDEX],
                          "Baker": [d.BREAD_INDEX],
                          "Brewer": [d.BEER_INDEX],
                          "Lumberjack": [d.LUMBER_INDEX],
                          "Carpenter": [d.CHAIR_INDEX, d.TABLE_INDEX]}
        business = job.getBusiness()
        unit = job.getUnit()
        materialIndexList = jobProductLink[job.getJobType()]

        for i in materialIndexList:
            amount = 10
            craftOrder = business.craftOrderManager(job, i)
            craftOrder.setAmount(10)

            transferOrder = business.transferOrderManager(unit, i)
            transferOrder.setAmount(10)

    # TODO-DONE get ai to build things other than bakery line.
    def buildIt(self, business, locality, toBuild):
        if toBuild.zoningType == "f":
            unitLocation = locality.find_sized_property(zone=toBuild.zoningType, xsize=5, ysize=5)
        else:
            unitLocation = locality.find_property(zone=toBuild.zoningType)

        if unitLocation is not None:
            existingUnits = business.getUnits()
            nonesuch = True

            for unit in existingUnits:
                unitType = unit.getUnitType()

                if (unitType == toBuild.unitType):
                    nonesuch = False

            if nonesuch:
                unitName = business.owners[0].lastname + " " + toBuild.unitType
                newUnit = toBuild(unitName, locality, unitLocation, business)
                if toBuild.zoningType == "f":
                    locality.claim_nodes_from_topleft(unitLocation, xsize=5, ysize=5, entity=newUnit)
                else:
                    locality.claim_node(unitLocation, newUnit)
                # self.initial_demand(newUnit)
                new_jobs = self.jobMaker(newUnit)
                for new_job in new_jobs:
                    self.craftOrderMaker(new_job)
                if newUnit.unitType == "Farm":
                    self.giveGrain(newUnit)

    # TODO farms should be multiple contiguous plots, each plot is one acre.
    # TODO start with prebuilt farms with existing grain stocks, not giving grain to new farms.
    def giveGrain(self, unit):
        unit.addStock(d.GRAIN_INDEX, 100000)

    # TODO for now, there is no startup cost
    def buildChain(self, business, toBuild):
        locality = business.getLocality()

        chains = [
            [u.Farm],
            [u.Mill, u.Farm],
            [u.Brewery, u.Farm],
            [u.Bakery, u.Mill, u.Farm],
            [],
            [],
            [u.Lumberyard],
            [u.Joinery, u.Lumberyard],
            [u.Joinery, u.Lumberyard]
        ]
        
        if toBuild is not None:
            for target in chains[toBuild]:
                self.buildIt(business, locality, target)

    # TODO boss or bank should front capital (much less than 1 million, too).
    def newBusiness(self, boss, busiName=None, capital=1000000):
        newBus = None

        if busiName is None:
            busiName = boss.lastname + " " + random.choice(d.busiNameList)

        if boss.capital >= capital:
            boss.capital -= capital
            newBus = bu.Business([boss], busiName, boss.locality, capital)
            boss.businesses.append(newBus)

            startupHQ = boss.getHome()

            OwnerJob = jobs.Owner(newBus, startupHQ)

            self.model.hirer.jobApplication(boss, OwnerJob)

            if boss != self.model.char:
                i_build = self.model.startupAI.whatToBuild(boss)
                self.model.builder.buildChain(boss.businesses[0], i_build)

        return newBus


class Character(p.People):
    def __init__(self, model, firstname, lastname, theirGender, theirHometown, theirHome,theirReligion):
        p.People.__init__(self, model, firstname, lastname, theirGender, theirHometown, theirHome, theirReligion)

    def startBusiness(self, busiName, capital=3000):
        newBusiness = self.model.builder.newBusiness(self, busiName, capital)

        return newBusiness

    # def build(self, business, unit, unitName):
    #     units = {"farm" : u.Farm, "bakery" : u.Bakery, "mill" : u.Mill, "warehouse" : u.Warehouse, "church" : u.Church}
    #     if business in self.businesses:
    #         newUnit = units[unit](unitName, business.getLocality(), business)
    #
    #     return newUnit

    def run_day(self):
        self.model.clock.runDay()


class ProductionAI(object):
    def __init__(self, model):
        self.model = model

    # TODO-DONE job should have can_make, not unit
    def setProduction(self, business):
        for job in business.getCraftingJobs():
            jobUnit = job.getUnit()
            demand  = jobUnit.getTotalDemand()

            for i in range(len(demand)):
                if job.can_make[i] and demand[i] > 0:
                    # crafted
                    if d.is_crafted(i):
                        self.setCraftOrder(business, job, demand[i], i)

                    # planted
                    elif d.is_planted(i):
                        self.setPlantOrder(business, job, i)
                        self.setHarvestOrder(business, job, i)

    def setCraftOrder(self, business, job, demand, i):
        jobUnit = job.getUnit()
        order = business.craftOrderManager(job, i)
        transfer = business.transferOrderManager(jobUnit, i)

        sellDemand = jobUnit.sales[i] + jobUnit.failSales[i]
        
        for component in d.getComponents(i):
            transport = business.transportOrderManager(jobUnit, component[0])
            
            if transport is not None:
                needed = component[1] * demand
                transport.setAmount(needed)
            else:
                # build unit?
                pass

        # TODO reduce amount if demand drops
        # they just flood the market if demand drops, which should raise demand. Nice and simple.
        if order.getAmount() < demand:
            order.setAmount(demand)
            transfer.setAmount(sellDemand)

    def setPlantOrder(self, business, job, i):
        jobUnit = job.getUnit()
        order = business.craftOrderManager(job, i)
        transfer = business.transferOrderManager(jobUnit, i)

        grow_days = jobUnit.incubator.getGrowDays(i)
        avgDemand = jobUnit.bigdata.getAvgDemand(i)
        # ratio = jobUnit.incubator.getRatio(i)
        # amount = avgDemand / ratio
        amount = avgDemand

        # get components- does nothing if none.
        for component in d.getComponents(i):
            transport = business.transportOrderManager(jobUnit, component[0])

            if transport is not None:
                needed = component[1] * amount
                transport.setAmount(needed)
            else:
                # build unit?
                pass

        total_amount = amount * grow_days
        # If there's a planting season for the material, we need a full year's worth.
        if d.seasons[i] != "all":
            total_amount = amount * 256

        if order.getAmount() < total_amount:
            order.setAmount(total_amount)
            # TODO transfer should allow "reserve" so we don't sell all our seeds.
            transfer.setAmount(avgDemand)

    def setHarvestOrder(self, business, job, i):
        order = business.harvestOrderManager(job, i)


class JobPoster(object):
    def __init__(self, model):
        self.model = model

    # TODO slots should not go above unit available slots
    # don't fire anyone for now, just go bankrupt- that's fine. AI is loyal. (Otherwise they may not get them back.)
    def managePositions(self, job):
        slots           = job.slots
        employees       = job.employees
        totalWorkers    = 0

        for order in (x for x in job.business.craftOrders if x.job == job):
            amount          = order.amount
            materialIndex   = order.materialIndex
            tech            = job.unit.getTech(materialIndex)

            if d.is_planted(materialIndex):
                # divide by length of planting season, not grow_days- how?
                grow_days = job.unit.incubator.getGrowDays(materialIndex)
                workers = math.ceil(amount / (tech * grow_days))

            elif d.is_crafted(materialIndex):
                workers = math.ceil(amount / tech)
            
            totalWorkers += workers

        newSlots = totalWorkers - len(job.employees)
        job.setSlots(newSlots if newSlots > 0 else 0)


class Hirer(object):
    def __init__(self, model):
        self.model = model

    # later, be more selective
    def jobApplication(self, nominee, job):
        isHired = self.hire(nominee, job)
        return isHired

    def hire(self, hiree, job):
        isHired = False
        business = job.business
        jobSlots = job.getSlots()
        employeeList = job.getEmployees()

        if (jobSlots >= 1):
            if (hiree.getJob() == None):
                isHired = True
                hiree.setJob(job, job.salary)
                job.decrementSlots()
                employeeList.append(hiree)
                business.m_employees.append(hiree)
                business.incrementHired(job.salary)

        # thoughts
        if isHired:
            hiree.think("I got hired by " + business.name + " as a " + job.jobType + ". I'll be working at " + job.unit.name + ".")
        else:
            hiree.think(job.business.name + " tried to hire me as a " + job.jobType + ", but it didn't work out.")

        return isHired


# never used- no one is ever fired and that's okay.
class Firer(object):
    def __init__(self, model):
        self.model = model

    def fire(self, firee, job):
        isFired = False
        fireeJob = firee.getJob()
        business = fireeJob.getUnit().getBusiness()

        if (fireeJob == job):
            isFired = True
            firee.unsetJob()
            job.incrementSlots()

            employeeList = job.getEmployees()
            employeeList.remove(firee)
            business.m_employees.remove(firee)

            for employee in employeeList:
                fireeNewJob = firee.getJob()
                #update employee's profile of firee
                fireeProfile = employee.peopleManager(firee)
                dayNum = job.unit.locality.clock.getDayNum()

                fireeProfile.updateJob(fireeNewJob, dayNum)

        if isFired:
            firee.think("I got fired from my job today.")

        return isFired


class SalaryPayer(object):
    def __init__(self, model):
        self.model = model

    def paySalaries(self):
        for unit in d.getUnit():
            laborCost = 0

            for job in unit.getJobList():
                totalSalary = 0
                totalEmployees = 0
                allWell = True

                # calculate
                for employee in job.employees:
                    # empBusiness = employee.getJob().getUnit().getBusiness()
                    salary = employee.getSalary()

                    # if (empBusiness == job.business):
                    totalSalary += salary
                    totalEmployees += 1
                    # else:
                    #     allWell = False

                # validate and pay
                if job.business.canAfford(totalSalary):
                    job.business.pay(totalSalary)

                    for employee in job.employees:
                        employee.addCapital(salary)

                        employee.think("I got paid " + str(salary) + " ducats today by " + job.business.name + ".")
                else:
                    allWell = False

                # unit needs totalSalary to calculate labor costs- if not paid, no cost, right?
                if allWell == False:
                    totalSalary = 0

                laborCost += totalSalary

            unit.setLaborTotal(laborCost)
