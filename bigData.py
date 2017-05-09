import database as d

class BigData(object):

    def __init__(self, model):
        self.avgPrices  = [0 for i in d.getMaterials()]
        self.sales      = [0 for i in d.getMaterials()]
        self.model      = model

    def addSale(self, materialIndex, amount, price):

        mean    = self.avgPrices[materialIndex]
        n       = self.sales[materialIndex]

        self.avgPrices[materialIndex] = (mean * (n / (n + amount))) + ((price * amount) / (n + amount))
        self.sales[materialIndex]    += amount

    def getData(self):
        businesses  = d.getBusinesses()
        units       = d.getUnit()
        people      = d.getPeople()
        return (businesses, units, people, self.avgPrices, self.sales)

#test
testData = BigData(None)
print(testData.sales, testData.avgPrices)
testData.addSale(3,15, 5)
print(testData.sales, testData.avgPrices)
testData.addSale(3,10, 3)
print(testData.sales, testData.avgPrices)
testData.addSale(3,0,4)
print(testData.sales, testData.avgPrices)
print(testData.getData())