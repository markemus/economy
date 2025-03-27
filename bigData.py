import copy
import numpy as np

import database as d

#bigdata makes SHALLOW COPIES of all lists passed to it.
class bigdata(object):
    def __init__(self, unit):
        self.unit       = unit
        self.locality   = unit.getLocality()
        self.sales      = []
        self.failSales  = []
        self.price      = []
        self.oPrice     = []
        self.crafted    = []
        self.customers  = []
        self.planted    = []
        self.harvested  = []
        self.DMC        = []
        self.stock      = []
        self.output     = []
        self.transports = []
        self.failTransports = []
    
    def getData(self, dayNum):
        values_dict = {}

        for key in ("sales", "price", "customers", "planted", "crafted", "harvested"):
            try:
                values_dict[key] = getattr(self, key)[dayNum]
            except (KeyError, IndexError):
                values_dict[key] = None

        return values_dict

    #i = materialIndex
    def getMonth(self, i):
        dayNum = self.getDayNum()
        days = []
        # TODO-DONE no fake days for first thirty
        lastThirty= ((dayNum - 29, dayNum) if dayNum > 29 else (0, dayNum))

        for key in ("price", "DMC", "crafted", "sales", "failSales", "transports", "failTransports", "stock", "output"):
            today = []
            
            for j in range(*lastThirty):
                try:
                    product = getattr(self, key)[j][i]
                except (KeyError, IndexError):
                    product = 0
                
                today.append(product)
            days.append(today)

        return days
    
    def getDayNum(self):
        return self.locality.getDayNum()

    def getRecentSales(self, days):
        return self.sales[-days:]

    def getRecentFailSales(self, days):
        return self.failSales[-days:]

    def getAvgSales(self, i):
        if len(self.sales) > 0:
            return sum([self.sales[day][i] for day in range(len(self.sales))]) / len(self.sales)
        else:
            return 0

    def getAvgFailSales(self, i):
        if len(self.failSales) > 0:
            return sum([self.failSales[day][i] for day in range(len(self.failSales))]) / len(self.failSales)
        else:
            return 0

    def getAvgTransports(self, i):
        if len(self.transports) > 0:
            return sum([self.transports[day][i] for day in range(len(self.transports))]) / len(self.transports)
        else:
            return 0

    def getAvgFailTransports(self, i):
        if len(self.failTransports) > 0:
            return sum([self.failTransports[day][i] for day in range(len(self.failTransports))]) / len(self.failTransports)
        else:
            return 0

    #works as long as all 4 arrays are the same length. Otherwise need weighted avg
    def getAvgDemand(self, i):
        return (self.getAvgSales(i) + self.getAvgFailSales(i) + self.getAvgTransports(i) + self.getAvgFailTransports(i))

    def updateSales(self, sales):
        self.sales.append(copy.copy(sales))

    def updateFailSales(self, failSales):
        self.failSales.append(copy.copy(failSales))

    def updatePrice(self, price):
        self.price.append(copy.copy(price))

    def updateOptimalPrice(self, oPrice):
        self.oPrice.append(copy.copy(oPrice))

    def updateCrafted(self, crafted):
        self.crafted.append(copy.copy(crafted))

    def updateCustomers(self, customers):
        self.customers.append(copy.copy(customers))

    def updatePlanted(self, planted):
        self.planted.append(copy.copy(planted))

    def updateHarvested(self, harvested):
        self.harvested.append(copy.copy(harvested))

    def updateDMC(self, DMC):
        self.DMC.append(copy.copy(DMC))

    def updateStock(self, stock):
        self.stock.append(copy.copy(stock))

    def updateOutput(self, output):
        self.output.append(copy.copy(output))

    def updateTransports(self, transports):
        self.transports.append(copy.copy(transports))

    def updateFailTransports(self, failTransports):
        self.failTransports.append(copy.copy(failTransports))