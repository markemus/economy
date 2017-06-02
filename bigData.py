import database as d

class bigdata(object):

    def __init__(self, unit):

        self.unit       = unit
        materials       = d.getMaterials()
        # self.avgPrices  = [0 for i in materials]
        self.sales      = []
        self.prices     = []
        self.crafted = []

    # def addSale(self, materialIndex, amount, price):

    #     mean    = self.avgPrices[materialIndex]
    #     n       = self.sales[materialIndex]

    #     self.avgPrices[materialIndex] = (mean * (n / (n + amount))) + ((price * amount) / (n + amount))
    #     self.sales[materialIndex]    += amount

    def update(self):
        self.sales.append(self.unit.sales)
        self.prices.append(self.unit.prices)
        self.crafted.append(self.unit.crafted)

    def getData(self):
        return (self.sales, self.prices, self.crafted)

# # test
# testData = bigdata(None)
# testData.sales.append([1,2,3])
# testData.sales.append([1,2,4])
# print(testData.sales)

# print(testData.sales, testData.avgPrices)
# testData.addSale(3,15, 5)
# print(testData.sales, testData.avgPrices)
# testData.addSale(3,10, 3)
# print(testData.sales, testData.avgPrices)
# testData.addSale(3,1,0)
# print(testData.sales, testData.avgPrices)
# print(testData.getData())
