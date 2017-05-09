import database as d
import business as bu
import unit as u
import people as p
import jobs

#singleton
class StartupAI(object):

    def __init__(self):
        None

    #O(n^2). Not ideal, but n SHOULD be low. Can we make O(n)?
    def whatToBuild(self, investor):
        # ratings = [0 for i in self.requiredStock]
        # prices = [0 for i in self.requiredStock]

        knownStock = self.knownStock(investor)
        #dummy ai will build full product lines, so all are equally possible.
        # possibilities = self.possibilities(investor, knownStock)
        possibilities = self.tempPossibilities(investor)
        optimalList = self.optimalList(investor)
        bestPossible = self.bestPossible(possibilities, optimalList)

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

    #which products can the investor find stock for?
    #O(n^2)- not exactly, but multivariate
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

    #people shop for the thing they want the most. So they want to open businesses with that in mind- what will bring in the most customers?
    def optimalList(self, investor):
        peopleProfiles = investor.getKnownPeople()
        highestMU = [0 for i in d.getMaterials()]

        for profile in peopleProfiles:
            #[0] because tuple
            muList = profile.getMuList()[0]
            maxMu = muList.index(max(muList))
            highestMU[maxMu] += 1

        return highestMU

    def bestPossible(self, possibilities, optimalList):
        notDone = True

        while notDone:
            bestOption = optimalList.index(max(optimalList))
            
            if optimalList[bestOption] == 0:
                bestOption = None
                notDone = False

            if bestOption is not None:
                if possibilities[bestOption]:
                    notDone = False
                else:
                    optimalList[bestOption] = 0

        return bestOption







#factory for supply chains. 
class Builder(object):
    availableProperty = (0,3)

    def __init__(self, model):
        self.model = model

    #I know it's terrible, okay? It's not meant to be good.
    def findProperty(self, locality):
        self.availableProperty = (self.availableProperty[0] + 1, self.availableProperty[1])
        return self.availableProperty

    def initial_demand(self, unit):
        for i in range(len(unit.can_make)):
            if unit.can_make[i]:
                unit.sales[i] = 10

    def jobMaker(self, unit):
        unitJobLink = { "Farm"      : jobs.Farmer,
                        "Brewery"   : jobs.Brewer,
                        "Mill"      : jobs.Miller,
                        "Bakery"    : jobs.Baker,
                        "Lumberyard": jobs.Lumberjack,
                        "Joinery"   : jobs.Carpenter}

        slots = 10
        salary = 40

        newJob = unitJobLink[unit.getUnitType()](slots, unit.getBusiness(), unit, 40)

        return newJob

    #also makes transfer orders
    def craftOrderMaker(self, job):
        jobProductLink = {"Farmer" : (d.GRAIN_INDEX,),
                          "Miller" : (d.FLOUR_INDEX,),
                          "Baker"  : (d.BREAD_INDEX,),
                          "Brewer" : (d.BEER_INDEX,),
                          "Lumberjack" : (d.WOOD_INDEX,),
                          "Carpenter" : (d.CHAIR_INDEX, d.TABLE_INDEX,)}
        business = job.getBusiness()
        materialIndexList = jobProductLink[job.getJobType()]

        for i in materialIndexList:
            amount = 10
            craftOrder = business.craftOrderManager(job, i)
            craftOrder.setAmount(10)
            self.model.jobPoster.managePositions(job, craftOrder)

            transferOrder = business.transferOrderManager(business.jobList[0], job.unit, i)
            transferOrder.setAmount(10)
        
    def buildIt(self, business, locality, toBuild):
        unitLocation = self.findProperty(locality)
        existingUnits = business.getUnits()
        nonesuch = True

        for unit in existingUnits:
            unitType = unit.getUnitType()

            if (unitType == toBuild.unitType):
                nonesuch = False

        if nonesuch:
            newUnit = toBuild(toBuild.unitType, locality, unitLocation, business)
            self.initial_demand(newUnit)
            new_job = self.jobMaker(newUnit)
            self.craftOrderMaker(new_job)

    #for now, there is no startup cost
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

    def newBusiness(self, boss):

        busiName = boss.getName() + "'s business"
        newBus = bu.Business([boss], busiName, boss.locality, 1000000)
        boss.businesses.append(newBus)

        startupHQ = boss.getHome()

        ManagerJob = jobs.Manager(newBus, startupHQ, 40)
        TransportJob = jobs.Carrier(1, newBus, startupHQ, 40)

        self.model.hirer.jobApplication(boss, ManagerJob)

        i_build = self.model.startupAI.whatToBuild(boss)
        self.model.builder.buildChain(boss.businesses[0], i_build)






class Character(p.People):
    
    def __init__(self, model, theirName, theirGender, theirAge, theirHometown, theirHome, theirSkills, theirReligion):
        p.People.__init__(self, model, theirName, theirGender, theirAge, theirHometown, theirHome, theirSkills, theirReligion)

    def startBusiness(self, busiName, cash):
        newBusiness = None
        if self.capital >= cash:
            newBusiness = bu.Business([self], busiName, self.locality, cash)
            self.businesses.append(newBusiness)

        return newBusiness

    def build(self, business, unit, unitName):
        units = {"farm" : u.Farm, "house" : u.House, "bakery" : u.Bakery, "mill" : u.Mill, "warehouse" : u.Warehouse, "church" : u.Church}
        if business in self.businesses:
            newUnit = units[unit](unitName, business.getLocality(), business)

        return newUnit

    def run_day(self):
        self.model.clock.runDay()







class ProductionAI(object):

    def __init__(self, model):
        self.model = model

    def setProduction(self, business):

        jobLists        = [business.getHarvestJobs(), business.getCraftingJobs()]
        orderManagers    = [business.harvestOrderManager, business.craftOrderManager]

        for x in range(len(jobLists)):
            
            jobList = jobLists[x]

            for job in jobList:
                jobUnit     = job.getUnit()
                unitDemand  = jobUnit.getTotalDemand()
                # unitStock   = jobUnit.getAllStock()

                for i in range(len(unitDemand)):
                    demand = unitDemand[i]

                    if demand > 0:
                        order = orderManagers[x](job, i)
                    
                        if order.getAmount() < demand:
                            order.setAmount(demand)
                            self.model.jobPoster.managePositions(job, order)






class JobPoster(object):

    def __init__(self, model):
        self.model = model

    def managePositions(self, job, order):
        slots           = job.getSlots()
        employees       = job.getEmployees()
        amount          = order.getAmount()
        materialIndex   = order.getProductIndex()
        unit            = job.getUnit()
        tech            = unit.getTech(materialIndex)
        totalSlots      = slots + len(employees)

        if (amount / tech) > (totalSlots):
            newSlots = round(amount / tech) - len(employees)
            job.setSlots(newSlots)







class Hirer(object):

    def __init__(self, model):
        self.model = model

    #later, be more selective
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

        #thoughts
        if isHired:
            hiree.think("I got hired by " + business.name + " as a " + job.jobType + ". I'll be working at " + job.unit.name + ".")
        else:
            hiree.think(job.business.name + " tried to hire me as a " + job.jobType + ", but it didn't work out.")

        return isHired







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

                #calculate
                for employee in job.employees:
                    # empBusiness = employee.getJob().getUnit().getBusiness()
                    salary = employee.getSalary()

                    # if (empBusiness == job.business):
                    totalSalary += salary
                    totalEmployees += 1
                    # else:
                    #     allWell = False

                #validate and pay
                if job.business.canAfford(totalSalary):
                    job.business.pay(totalSalary)

                    for employee in job.employees:
                        employee.addCapital(salary)

                        #thoughts
                        employee.think("I got paid " + str(salary) + " ducats today by " + job.business.name + ".")
                else:
                    allWell = False

                toString=("\nSalaries were paid by " + job.business.name + " to their " + job.jobType + "s." + 
                      "\nTotal amount:" +    str(totalSalary) +
                      "\nTotal employees:" + str(totalEmployees) +
                      "\nAll was well?" +    str(allWell) + "\n")
                self.model.out(toString)

                #unit needs totalSalary to calculate labor costs- if not paid, no cost, right?
                if allWell == False:
                    totalSalary = 0

                laborCost += totalSalary

            unit.setLaborTotal(laborCost)