import database as d
import jobs as j
import incubator as inc
import bigData as big
import staff

import copy

#Not all units, but all units you can create (no house, church)
def all_units():
    unit_list = [Farm, Mill, Brewery, Bakery, Lumberyard, Joinery]
    return unit_list

class Unit(object):
    unitType = "genericUnit"
    character = "X"
    locality = None     #should be a locality
    location = ()       #(x,y), being indices on the localMap.
    business = None
    # lists generated in __init__
    # [grain, flour, bread, beer]
    stock = None
    # [millstone]
    equipment = None
    # [grain, flour, bread, beer]
    output = None
    # money = 0
    #Boolean is clunky, but allows each unit to have multiple purposes- work from home, etc.
    isMarket = False

    def __init__ (self, unitName, unitLocality, unitLocationTuple, business):
        self.name       = unitName
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
        self.tech       = [0 for material in stockLength]
        #current prices
        self.price      = [0 for material in stockLength]
        self.purchases  = [0 for material in stockLength]
        #yesterday's number of sales for each item
        self.sales      = [0 for material in stockLength]
        self.failSales  = [0 for material in stockLength]
        #Direct Materials Cost of a SINGLE instance of each product
        self.DMC        = [0 for material in stockLength]
        # self.orders     = [0 for material in stockLength]
        self.crafted    = [0 for material in stockLength]
        self.missions   = [False for mission in missionsLength]
        self.can_make   = [False for material in stockLength]
        self.laborTotal = 0
        self.rentTotal  = 0

    # def __str__(self):
    #     return self.character

    def toString(self):
        print("------------------------------------------")
        print(self.name + " is a " + self.unitType + ".")
        print("\nCurrent stocks:")
        print("Stock:", self.stock)
        print("Output:", self.output)
        print("\nCurrent prices:")
        print("Direct material costs:", self.DMC)
        print("Total labor costs:", self.laborTotal)
        print("Total rent costs:", self.rentTotal)
        print("Sales:", self.sales)
        print("Prices:", self.price)

    def getPrice(self):
        return self.price

    # def sell(self, who, amount, i_item):
    #     if self.output[i_item] >= amount:
    #         thisPrice = self.price[i_item]

    #         who.addCapital(-thisPrice)
    #         self.business.addCash(thisPrice)
    #         who.addInventory(i_item, amount)
    #         self.addOutput(i_item, -amount)
            
    #         sold = True
    #     else:
    #         sold = False
        
    #     if sold:
    #         self.addSales(i_item, amount)
    #     else:
    #         self.addFailSales(i_item, amount)

    #     return sold

    def sell(self, who, amounts):
        sold = False
        cost = sum(self.price[i] * amounts[i] for i in range(len(self.output)))

        #verify
        if who.canAfford(cost):
            if (self.output[i] >= amounts[i] for i in range(len(self.output))):

                #sale
                who.addCapital(-cost)
                self.business.addCash(cost)
                
                for i in range(len(self.output)):
                    self.addOutput(i, -amounts[i])
                    who.addInventory(i, amounts[i])

                    self.addSales(i, amounts[i])

                    sold = True

        return sold

    #here be dragons
    #call AFTER transferring but BEFORE transporting. For stores, after restocking and before selling.
    #priceGen gives new prices every period for each item based on the earlier price and 
    #the "optimal price" that it should trend towards.
    def priceGen(self):
        oPrice = [0 for i in self.output]
        labor = [0 for i in self.output]
        rent = [0 for i in self.output]
        naturalPrice = [0 for i in self.output]
        #natural rate of profit- 4% return on capital
        nrp = 1.04
        #paid weekly, divide by workdays
        dailyLabor = (self.laborTotal / 5)
        #K is a constant weight- adjust if needed. At .5 one period is the half life.
        K = .5
        #DMC = direct materials cost
        totalDMC = 0

        #calculate total DMC
        for i in range(len(self.DMC)):
            totalDMC += (self.DMC[i] * self.crafted[i])

        if totalDMC != 0:

            for i in range(len(self.price)):
                if self.output[i] != 0:
                    #natural price
                    labor[i] =  dailyLabor * self.DMC[i] / totalDMC
                    rent[i] = self.rentTotal * self.DMC[i] / totalDMC
                    
                    naturalPrice[i] = (self.DMC[i] + labor[i] + rent[i]) * nrp

                    #if never sold before
                    if self.price[i] == 0:
                        self.price[i] = round(naturalPrice[i], 2)
                    else:
                        #optimal price, set price.
                        demand = self.sales[i] + self.failSales[i]
                        oPrice[i] = (demand / self.output[i]) * naturalPrice[i]
                        priceAdjustment = (K * (oPrice[i] - self.price[i]))
                        self.price[i] = round(self.price[i] + priceAdjustment, 2)

        # #debug
        # print("-----------------------")
        # print(self.name,"priceGen:")
        # print("\nSales:", self.sales)
        # print("Crafted:", self.crafted)
        # print("Stock:", self.stock)
        # print("Output:", self.output)
        # print("\nDMC:", self.DMC)
        # print("Total DMC:", totalDMC)
        # print("Daily labor", dailyLabor)
        # print("Labor:", labor)
        # print("Rent:", rent)
        # print("\nNatural price:", naturalPrice)
        # print("oPrice:", oPrice)
        # print("Price:", self.price)
        # print("")
        # #endDebug
        self.resetSales()

    def growingPlants(self, materialIndex):
        return self.incubator.getGrowing(d.getMaterials()[materialIndex])

    def ripePlants(self, materialIndex):
        return self.incubator.getRipe(d.getMaterials()[materialIndex])

    def plantSeeds(self, materialIndex, amount):
        if self.stock[materialIndex] <= amount:
            amount = self.stock[materialIndex]

        self.stock[materialIndex] -= amount
        self.incubator.plant(d.getMaterials()[materialIndex], amount)

    def harvest(self, materialIndex, amount):
        if self.ripePlants(materialIndex) >= amount:
            amount = self.incubator.harvest(d.getMaterials()[materialIndex], amount)
            self.addCrafted(materialIndex, amount)
            self.addStock(materialIndex, amount)
            #productDMC = 0 for now

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

    def getIsMarket(self):
        return self.isMarket

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

    def addPurchase(self, materialIndex, amount):
        self.purchases[materialIndex] += amount

    def addSales(self, materialIndex, amount):
        self.sales[materialIndex] += amount

    def addFailSales(self, materialIndex, amount):
        self.failSales[materialIndex] += amount

    def getTotalDemand(self):
        demand = []

        for i in range(len(self.sales)):
            demand.append(self.sales[i] + self.failSales[i])

        return demand

    def addStock(self, materialIndex, amount):
        self.stock[materialIndex] += amount

    def addOutput(self, materialIndex, amount):
        self.output[materialIndex] += amount

    def addCrafted(self, materialIndex, amount):
        self.crafted[materialIndex] += amount

    def getCrafted(self):
        return self.crafted

    #used for displaying production in matplotlib
    def getProduction(self):
        return ([0,1,2,3,4,5,6,7,8], self.crafted)
        
    # def addCapital(self, amount):
    #     self.money += amount

    def addJob(self, job):
        self.jobList.append(job)

    def removeJob(self, job):
        self.jobList.remove(job)

    def setDMC(self, materialIndex, DMCost):
        self.DMC[materialIndex] = DMCost

    def setLaborTotal(self, laborTotal):
        self.laborTotal = laborTotal

    def resetLaborTotal(self):
        self.laborTotal = 0

    def resetPurchases(self):
        self.purchases = [0 for i in self.purchases]
        
    def resetSales(self):
        self.sales      = [0 for i in self.sales]
        self.failSales  = [0 for i in self.failSales]

    def resetCrafted(self):
        self.crafted = [0 for i in self.crafted]

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
        self.tech[d.GRAIN_INDEX] = 16
        self.stock[d.GRAIN_INDEX] = 50
        self.DMC[d.GRAIN_INDEX] = 1
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)







class Mill(Manufactury):
    unitType = "Mill"
    character = "M"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.FLOUR_INDEX] = True
        self.tech[d.FLOUR_INDEX] = 40
        self.missions[d.MANU_INDEX] = True
        self.stock[d.GRAIN_INDEX] = 50
        self.DMC[d.GRAIN_INDEX] = 1
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)







class Brewery(Manufactury):
    unitType = "Brewery"
    character = "b"

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.BEER_INDEX] = True
        self.tech[d.BEER_INDEX] = 60
        self.missions[d.MANU_INDEX] = True
        self.stock[d.GRAIN_INDEX] = 50
        self.DMC[d.GRAIN_INDEX] = 1
        d.addUnit(self)
        if self.business is not None:
            self.business.addUnit(self)







class Bakery(Manufactury):
    unitType = "Bakery"
    character = "B"
    # isMarket = True

    def __init__(self, unitName, unitLocality, unitLocationTuple, business):
        Manufactury.__init__(self, unitName, unitLocality, unitLocationTuple, business)
        self.can_make[d.BREAD_INDEX] = True
        self.tech[d.BREAD_INDEX] = 10
        self.missions[d.MANU_INDEX] = True
        self.missions[d.STORE_INDEX] = True
        self.stock[d.FLOUR_INDEX] = 50
        self.DMC[d.FLOUR_INDEX] = 1

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
        self.DMC[d.WOOD_INDEX] = 1
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
        self.DMC[d.WOOD_INDEX] = 1
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