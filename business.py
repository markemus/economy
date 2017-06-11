import database as d
import orders as o

#composed of Units
class Business(object):
    name = "businessName"
    cash = 0
    locality = None

    def __init__(self, owners, name, busiLocality, busiCash):
        self.owners             = owners
        self.name               = name
        self.locality           = busiLocality
        self.model              = self.locality.model
        self.cash               = busiCash
        self.m_unitList         = []
        self.m_employees        = []
        self.jobList            = []
        self.craftingJobs       = []
        self.harvestJobs        = []
        self.priestJobs         = []
        self.harvestOrders      = []
        self.craftOrders        = []
        self.transferOrders     = []
        self.transportOrders    = []
        self.pricingOrders      = []
        self.model              = self.locality.model
        self.dailyHired         = 0
        self.newTotalSalaries   = 0
        d.addBusiness(self)

    def addCash(self, amount):
        self.cash += amount

    def getJobs(self):
        return self.jobList

    def addJob(self, job):
        self.jobList.append(job)

    def addCraftingJob(self, job):
        self.craftingJobs.append(job)

    def getCraftingJobs(self):
        return self.craftingJobs

    def addHarvestJob(self, job):
        self.harvestJobs.append(job)

    def addPriestJob(self, job):
        self.priestJobs.append(job)

    def getPriestJobs(self):
        return self.priestJobs

    def getHarvestJobs(self):
        return self.harvestJobs

    def getCraftOrders(self):
        return self.craftOrders

    def getTransferOrders(self):
        return self.transferOrders

    def getTransportOrders(self):
        return self.transportOrders

    #addUnit should be called AFTER missions assignment.
    def addUnit(self, unit):
        self.m_unitList.append(unit)
        self.pricingOrders.append(o.pricingOrder(self, unit.staff.manager, unit))
        for owner in self.owners:
            owner.unitManager(unit)

            #they tell all their friends about their new venture.
            for friend in owner.knownPeople:
                friend.person.unitManager(unit)

    def removeJob(self, job):
        self.jobList.remove(job)

    def removeOrder(self, order):
        self.orders.remove(order)

    def removeUnit(self, unit):
        self.m_unitList.remove(unit)
        #remove unit's pricing order here

    def pay(self, amount):
        self.cash -= amount 

    def getProduction(self):
        crafted = [0,0,0,0,0,0,0,0,0]
        for unit in self.m_unitList:
            thisCrafted = unit.getCrafted()

            for i in range(len(thisCrafted)):
                crafted[i] +=  thisCrafted[i]

        return ([0,1,2,3,4,5,6,7,8], crafted)

    def getAllStock(self):
        stock = [0,0,0,0,0,0,0,0,0]
        for unit in self.m_unitList:
            thisStock = unit.getAllStock()

            for i in range(len(thisStock)):
                stock[i] += thisStock[i]

        return stock

    def getCash(self):
        return self.cash

    def getName(self):
        return self.name

    def getLocality(self):
        return self.locality

    def getUnits(self):
        return self.m_unitList

    #was getEmployees
    def get_emp_dict(self):
        empDict = {}

        for unit in self.m_unitList:
            empDict[unit] = unit.getEmployees() 
            
        return empDict

    def getHired(self):
        return (self.dailyHired, self.newTotalSalaries)

    def incrementHired(self, salary):
        self.dailyHired += 1
        self.newTotalSalaries += salary

    def resetHired(self):
        self.dailyHired = 0
        self.newTotalSalaries = 0

    def canAfford(self, amount):
        can = False
        if self.cash >= amount:
            can = True
        return can

    def hiredOut(self):
        toString =  (
            "\n" + self.name + 
            " hired " + str(self.dailyHired) +  
            " new employees today. Total salaries: $" + str(self.newTotalSalaries) + 
            ".")
        return toString

    def harvestOrderManager(self, job, productIndex):
        noOrder = True

        for thisOrder in self.harvestOrders:
            if (thisOrder.getJob() == job) and (thisOrder.getProductIndex() == productIndex):
                targetOrder = thisOrder
                noOrder = False
                break

        if noOrder:
            targetOrder = o.harvestOrder(self, job, productIndex)
            self.harvestOrders.append(targetOrder)

        return targetOrder

    def craftOrderManager(self, job, productIndex):
        noOrder = True

        for thisOrder in self.craftOrders:
            if (thisOrder.getJob() == job) and (thisOrder.getProductIndex() == productIndex):
                targetOrder = thisOrder
                noOrder = False
                break

        if noOrder:
            targetOrder = o.craftOrder(self, job, productIndex)
            self.craftOrders.append(targetOrder)

        return targetOrder

    def transportOrderManager(self, job, startUnit, endUnit, productIndex):
        noOrder = True

        for thisOrder in self.transportOrders:
            if (thisOrder.getJob() == job) and (thisOrder.getProductIndex() == productIndex):
                if (thisOrder.getStartUnit() == startUnit) and (thisOrder.getEndUnit() == endUnit):
                    targetOrder = thisOrder
                    noOrder = False
                    break

        if noOrder:
            targetOrder = o.transportOrder(self, job, startUnit, endUnit, productIndex)
            self.transportOrders.append(targetOrder)

        return targetOrder

    def transferOrderManager(self, job, unit, productIndex):
        noOrder = True

        for thisOrder in self.transferOrders:
            if (thisOrder.getJob() == job) and (thisOrder.getProductIndex() == productIndex):
                if (thisOrder.getUnit() == unit):
                    targetOrder = thisOrder
                    noOrder = False
                    break
        if noOrder:
            targetOrder = o.transferOrder(self, job, unit, productIndex, 0)
            self.transferOrders.append(targetOrder)

        return targetOrder

    def workHandler(self):
        self.resetHired()

        for unit in self.m_unitList:
            unit.resetCrafted()
            unit.resetPurchases()
            unit.incubator.next_day()

        for order in self.harvestOrders:
            order.execute()
        for order in self.craftOrders:
            order.execute()
        for order in self.transferOrders:
            order.execute()

    def restHandler(self):
        for order in self.pricingOrders:
            order.execute()

    def shopHandler(self):
        for order in self.transportOrders:
            order.execute()
        for unit in self.m_unitList:
            unit.bigdata.update()