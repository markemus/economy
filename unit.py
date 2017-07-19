import database as d
import jobs as j
import incubator as inc
import bigData as big
import staff

import copy
import math

#Not all units, but all units you can create (no house, church)
def all_units():
    unit_list = [Farm, Mill, Brewery, Bakery, Lumberyard, Joinery]
    return unit_list

#units use Business's money
class Unit(object):
    unitType = "genericUnit"
    character = "X"
    locality = None     #should be a locality
    location = ()       #(x,y), being indices on the localMap.
    business = None
    stock = None
    output = None

    def __init__ (self, unitName, unitLocality, unitLocationTuple, business):
        self.name       = unitName
        self.bigdata    = big.bigdata(self)
        stockLength     = range(len(d.getMaterials()))
        missionsLength  = range(len(d.getUnitMissions()))
        self.locality   = unitLocality
        self.location   = unitLocationTuple
        self.business   = business
        self.jobList    = []
        self.incubator  = inc.incubator(self)
        self.bigdata    = big.bigdata(self)
        self.stock      = [0 for material in stockLength]
        self.output     = [0 for material in stockLength]
        self.tech       = [1 for material in stockLength]
        #current prices
        self.price      = [0 for material in stockLength]
        self.purchases  = [0 for material in stockLength]
        #yesterday's number of sales for each item
        self.sales      = [0 for material in stockLength]
        self.failSales  = [0 for material in stockLength]
        self.transports = [0 for material in stockLength]
        self.failTransports = [0 for material in stockLength]
        #Direct Materials Cost of a SINGLE instance of each product
        self.DMC        = [0 for material in stockLength]
        # self.orders     = [0 for material in stockLength]
        self.crafted    = [0 for material in stockLength]
        self.planted    = [0 for material in stockLength]
        self.harvested  = [0 for material in stockLength]
        self.missions   = [False for mission in missionsLength]
        self.can_make   = [False for material in stockLength]
        self.laborTotal = 0
        # self.rentTotal  = 0
        self.customers  = []

    def toString(self):
        print("------------------------------------------")
        print(self.name + " is a " + self.unitType + ".")
        print("\nCurrent stocks:")
        print("Stock:", self.stock)
        print("Output:", self.output)
        print("\nCurrent crafted:")
        print("Crafted: ", self.crafted)
        print("Planted: ", self.planted)
        print("\nCurrent prices:")
        print("Direct material costs:", self.DMC)
        print("Last week's labor costs:", self.laborTotal)
        print("Sales:", self.sales)
        print("Failsales: ", self.failSales)
        print("Demand: ", [self.sales[i] + self.failSales[i] for i in range(len(self.sales))])
        print("Prices:", self.price)

    def getPrice(self):
        return self.price

    def complain(self, who):
        failSale = [0 for i in range(len(d.getMaterials()))]
        cost = 0

        self.customers.append((who, failSale, copy.copy(self.output), cost, who.capital, False))

    def sell(self, who, amounts):
        wishamounts = copy.copy(amounts)
        wishcost = sum(self.price[i] * wishamounts[i] for i in range(len(self.output)))

        for i in range(len(self.output)):
            if amounts[i] > self.output[i]:
                amounts[i] = math.floor(self.output[i])

        cost = sum(self.price[i] * amounts[i] for i in range(len(self.output)))

        #verify
        if who.canAfford(cost):
            #sale
            who.addCapital(-cost)
            self.business.addCash(cost)
            
            for i in range(len(self.output)):
                self.addOutput(i, -amounts[i])
                who.addInventory(i, amounts[i])

                self.addSales(i, amounts[i])
                self.addFailSales(i, wishamounts[i] - amounts[i])
        
        if sum(amounts) > 0:
            sold = True
        else:
            sold = False

        #customers is for bigData- cleared during *PHASE*
        self.customers.append((who, wishamounts, wishcost, copy.copy(amounts), cost, copy.copy(self.output), who.capital, sold))

        return (amounts, cost, sold)

    #calculate the price of a single material, without changing it in place- i = materialIndex
    def priceCalc(self, i):
        #natural rate of profit- 4% return on capital
        nrp = 1.04
        #K is a constant weight- adjust if needed. At .5 one period is the half life.
        K = .5
        
        #natural price
        if d.getMaterials()[i] in d.planted:
            #2 days, tech same for planting and harvesting
            ratio = self.incubator.ratios[d.getMaterials()[i]]
            labor = 2 / (self.tech[i] * ratio)
        else:
            labor = 1 / self.tech[i]

        naturalPrice = (self.DMC[i] + labor) * nrp

        #if never sold before
        if self.price[i] == 0:
            price = round(naturalPrice, 2)
            oPrice = price

        #if sold before
        else:
            #optimal price, set price.
            demand = self.sales[i] + self.failSales[i]
            oPrice = (demand / self.output[i]) * naturalPrice
            priceAdjustment = (K * (oPrice - self.price[i]))
            price = round(self.price[i] + priceAdjustment, 2)

        return (price, oPrice, naturalPrice)

    #call AFTER transferring but BEFORE transporting. For stores, after restocking and before selling. (rest)
    #priceGen gives new prices every period for each item based on the earlier price and 
    #the "optimal price" that it should trend towards.
    def priceGen(self):
        yDayNum = self.getDayNum() - 1
        oPrice = [0 for i in d.getMaterials()]
        naturalPrice = [0 for i in d.getMaterials()]

        for i in range(len(self.price)):
            if self.output[i] != 0:
                (self.price[i], oPrice[i], naturalPrice[i]) = self.priceCalc(i)
        #debug
        # if self.name in ("Bill's Farm", "Bill's Mill", "Bill's Bakery"):
        #     print(self.name)
        #     print("DMC:    ", self.DMC)
        #     print("sales:  ", self.sales)
        #     print("output: ", self.output)
        #     print("nPrice: ", naturalPrice)
        #     print("oPrice: ", oPrice)
        #     print("price:  ", self.price)
        #     print("")

        self.resetSales()
        self.resetCustomers()

    def growingPlants(self, materialIndex):
        return self.incubator.getGrowing(d.getMaterials()[materialIndex])

    def ripePlants(self, materialIndex):
        return self.incubator.getRipe(d.getMaterials()[materialIndex])

    def plantSeeds(self, materialIndex, amount):
        # if self.stock[materialIndex] <= amount:
        #     amount = self.stock[materialIndex]

        # self.stock[materialIndex] -= amount
        self.incubator.plant(d.getMaterials()[materialIndex], amount)

    def harvest(self, materialIndex, amount):
        if self.ripePlants(materialIndex) >= amount:
            amount = self.incubator.harvest(d.getMaterials()[materialIndex], amount)
            self.addCrafted(materialIndex, amount)
            self.addStock(materialIndex, amount)

    def getName(self):
        return self.name

    def getEmployees(self):
        employeeList = []

        for job in self.jobList:
            employeeList += job.getEmployees()

        return employeeList

    def get_emp_dict(self):
        empDict = {}

        for job in self.jobList:
            empDict[job] = job.getEmployees()

        return empDict

    def getLocality(self):
        return self.locality

    def getLocation(self):
        return self.location

    def getBusiness(self):
        return self.business

    def getDayNum(self):
        return self.locality.getDayNum()

    def getDMC(self):
        return self.DMC

    # def getIsMarket(self):
    #     return self.isMarket

    #for now, skills don't matter. But they will.
    def getJobs(self, interviewee):
        jobList = copy.copy(self.jobList)
        return jobList

    def getJobList(self):
        return self.jobList

    def getOutput(self, materialIndex):
        return (self.output[materialIndex])

    def getAllOutput(self):
        return self.output

    def getMissions(self):
        return self.missions

    def getStock(self, materialIndex):
        return (self.stock[materialIndex])

    def getAllStock(self):
        return self.stock

    def getTech(self, materialIndex):
        return self.tech[materialIndex]

    def getUnitType(self):
        return self.unitType

    def setBusiness(self, newBusiness):
        self.business = newBusiness

    #addPurchase, addSales, addFailSales. This is stupid.
    def addPurchase(self, materialIndex, amount):
        self.purchases[materialIndex] += amount

    def addSales(self, materialIndex, amount):
        self.sales[materialIndex] += amount

    def addFailSales(self, materialIndex, amount):
        self.failSales[materialIndex] += amount

    def addTransports(self, materialIndex, amount):
        self.transports[materialIndex] += amount

    def addFailTransports(self, materialIndex, amount):
        self.failTransports[materialIndex] += amount

    def getTotalDemand(self):
        demand = []

        for i in range(len(self.sales)):
            demand.append(self.sales[i] + self.failSales[i] + self.transports[i] + self.failTransports[i])

        return demand

    def addStock(self, materialIndex, amount):
        self.stock[materialIndex] += amount

    def addOutput(self, materialIndex, amount):
        self.output[materialIndex] += amount

    def addCrafted(self, materialIndex, amount):
        self.crafted[materialIndex] += amount

    def addPlanted(self, materialIndex, amount):
        self.planted[materialIndex] += amount

    def addHarvested(self, materialIndex, amount):
        self.harvested[materialIndex] += amount

    def getCrafted(self):
        return self.crafted

    #used for displaying production in matplotlib
    def getProduction(self):
        return ([0,1,2,3,4,5,6,7,8], self.crafted)

    def getSales(self):
        return ([0,1,2,3,4,5,6,7,8], self.sales)

    def addJob(self, job):
        self.jobList.append(job)

    def removeJob(self, job):
        self.jobList.remove(job)

    def setDMC(self, materialIndex, DMCost):
        self.DMC[materialIndex] = DMCost

    def setLaborTotal(self, laborTotal):
        self.laborTotal = laborTotal

    def resetPurchases(self):
        self.purchases = [0 for i in self.purchases]
        
    def resetSales(self):
        self.sales          = [0 for i in self.sales]
        self.failSales      = [0 for i in self.failSales]
        self.transports     = [0 for i in self.transports]
        self.failTransports = [0 for i in self.failTransports]

    def resetCrafted(self):
        self.crafted = [0 for i in self.crafted]

    def resetPlanted(self):
        self.planted = [0 for i in self.planted]

    def resetHarvested(self):
        self.harvested = [0 for i in self.harvested]

    def resetCustomers(self):
        self.customers = []

    def getRevenue(self):
        revenue = []
        for i in range(len(self.sales)):
            thisRev = round(self.sales[i] * self.price[i], 2)
            revenue.append(thisRev)
        return revenue

    def dailyRevenue(self):
        materials = d.getMaterials()
        revenue = self.getRevenue()
        noSales = True

        toString = ("\n" + self.name + " made")
        for i in range(len(revenue)):
            if revenue[i] != 0:

                if not noSales:
                    toString += ","
                
                toString += (
                    " $" + str(revenue[i]) +
                    " from " + str(self.sales[i]) +
                    "/" + str(self.sales[i] + self.failSales[i]) +
                    " sales of " + materials[i]
                    )

                noSales = False
        
        toString += "."

        if noSales:
            toString = ("\n" + self.name + " made no sales today.")
        
        return toString

    def dailyCrafted(self):
        materials = d.getMaterials()
        toString = ("\n" + self.name + " created")
        noCrafted = True

        for i in range(len(self.crafted)):
            if self.crafted[i] != 0:

                if not noCrafted:
                    toString += ","

                toString += (
                    " " +
                    str(self.crafted[i]) + 
                    " " + str(materials[i])
                    )

                noCrafted = False

        toString += "."

        if noCrafted:
            toString = ("\n" + self.name + " didn't craft anything today.")

        return toString

    def dailyExpenses(self):
        pass




class Manufactury(Unit):
    unitType = "Manufactury"
    character = "Manu"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Unit.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.missions[d.MANU_INDEX] = True
        self.staff = staff.manu_staff(self)




class Farm(Manufactury):
    unitType = "Farm"
    character = "F"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.GRAIN_INDEX] = True
        self.tech[d.GRAIN_INDEX] = 4.5
        self.stock[d.GRAIN_INDEX] = 50
        # self.DMC[d.GRAIN_INDEX] = 1
        self.failSales[d.GRAIN_INDEX] = 500
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)



#20-30 kg flour per hour- ~440 lb per 8 hours
class Mill(Manufactury):
    unitType = "Mill"
    character = "M"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.FLOUR_INDEX] = True
        self.tech[d.FLOUR_INDEX] = 440
        self.missions[d.MANU_INDEX] = True
        self.stock[d.GRAIN_INDEX] = 50
        # self.DMC[d.GRAIN_INDEX] = 1
        self.failSales[d.FLOUR_INDEX] = 500
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class Brewery(Manufactury):
    unitType = "Brewery"
    character = "b"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.BEER_INDEX] = True
        self.tech[d.BEER_INDEX] = 40
        self.missions[d.MANU_INDEX] = True
        self.stock[d.GRAIN_INDEX] = 50
        # self.DMC[d.GRAIN_INDEX] = 1
        self.failSales[d.BEER_INDEX] = 500
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class Bakery(Manufactury):
    unitType = "Bakery"
    character = "B"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.BREAD_INDEX] = True
        self.tech[d.BREAD_INDEX] = 60
        self.missions[d.MANU_INDEX] = True
        self.missions[d.STORE_INDEX] = True
        self.stock[d.FLOUR_INDEX] = 50
        # self.DMC[d.FLOUR_INDEX] = 1
        self.failSales[d.BREAD_INDEX] = 500

        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class Lumberyard(Manufactury):
    unitType = "Lumberyard"
    character = "L"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.WOOD_INDEX] = True
        self.tech[d.WOOD_INDEX] = 50
        self.missions[d.MANU_INDEX] = True
        self.stock[d.WOOD_INDEX] = 50
        # self.DMC[d.WOOD_INDEX] = 1
        self.failSales[d.WOOD_INDEX] = 500
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class Joinery(Manufactury):
    unitType = "Joinery"
    character = "J"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.CHAIR_INDEX] = True
        self.can_make[d.TABLE_INDEX] = True
        self.tech[d.CHAIR_INDEX] = 1
        self.tech[d.TABLE_INDEX] = 1
        self.missions[d.MANU_INDEX] = True
        self.missions[d.STORE_INDEX] = True
        self.stock[d.WOOD_INDEX] = 50
        # self.DMC[d.WOOD_INDEX] = 1
        self.failSales[d.CHAIR_INDEX] = 500
        self.failSales[d.TABLE_INDEX] = 500
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class House(Unit):
    unitType = "Home"
    character = "H"

    def __init__(self, unitLocality, unitLocationTuple, business=None, unitName="House"):
        Unit.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.missions[d.HOME_INDEX] = True
        self.tenants = set()
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)

    def addTenant(self, tenant):
        self.tenants.add(tenant)

    def removeTenant(self, tenant):
        self.tenants.remove(tenant)




#the ai don't need warehouses, players probably do.
class Warehouse(Unit):
    unitType = "Warehouse"
    character = "W"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Unit.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.missions[d.MANU_INDEX] = True
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)




class Church(Unit):
    unitType = "Church"
    character = "C"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business, religion):
        Unit.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.religion = religion
        self.missions[d.CHURCH_INDEX] = True
        self.flock = []
        self.attendance = []
        self.staff = staff.church_staff(self)
        # self.manager = j.Manager(business, self, 41)
        d.addChurch(self)
        if self.business is not None:
            self.business.addUnit(self)

    def attend(self, member):
        self.attendance.append(member)

    def getAttendance(self):
        return self.attendance

    def resetAttendance(self):
        self.attendance = []

    def getReligion(self):
        return self.religion

    def getFlock(self):
        return self.flock

    def addMember(self, member):
        self.flock.append(member)