import database as d
import abc

#Orders allow a Business to queue method calls from their Jobs in a particular order, to be performed daily.
class Order(object):

    def __init__(self, business, job):
        self.business   = business
        self.job        = job

    def getJob(self):
        return self.job

class harvestOrder(Order):

    def __init__(self, business, job, materialIndex, amount=1):
        Order.__init__(self, business, job)
        self.materialIndex  = materialIndex
        self.amount = amount

    def execute(self):
        self.job.harvest(self.materialIndex, self.amount)

    def getProductIndex(self):
        return self.materialIndex

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

class craftOrder(Order):

    def __init__(self, business, job, materialIndex, amount=1):
        Order.__init__(self, business, job)
        self.materialIndex  = materialIndex
        self.amount         = amount

    def execute(self):
        self.job.craft(self.materialIndex, self.amount)

    def getProductIndex(self):
        return self.materialIndex

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

class transportOrder(Order):

    def __init__(self, business, job, unit1, unit2, materialIndex, amount=1):
        Order.__init__(self, business, job)
        self.unit1          = unit1
        self.unit2          = unit2
        self.materialIndex  = materialIndex
        self.amount         = amount

    def execute(self):
        self.job.transportMats(self.unit1, self.unit2, self.materialIndex, self.amount)

    def getProductIndex(self):
        return self.materialIndex

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount
   
    def getStartUnit(self):
        return self.unit1

    def getEndUnit(self):
        return self.unit2

class transferOrder(Order):

    def __init__(self, business, job, unit, materialIndex, amount):
        Order.__init__(self, business, job)
        self.unit           = unit
        self.materialIndex  = materialIndex
        self.amount         = amount

    def execute(self):
        self.job.transferMats(self.unit, self.materialIndex, self.amount)

    def getUnit(self):
        return self.unit

    def getProductIndex(self):
        return self.materialIndex

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

class pricingOrder(Order):

    def __init__(self, business, job, unit):
        Order.__init__(self, business, job)
        self.unit = unit

    def execute(self):
        self.job.updatePrices(self.unit)