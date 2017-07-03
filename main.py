import random
import cProfile

import ai
import business as b
import database as d
import gameMap as g
import generator as gen
import jobs as j
import orders as o
import people as p
import profiles as pr
import unit as u

from conversation import Convo
from gui import gui
from model import Model

#main

model = Model()
Jonestown = d.getLocality()[0]
model.week.machine.set_state('Friday')

#players
MrMoney = d.getPeople()[0]
MrsMoney = d.getPeople()[1]
you = model.gui.char

CatholicChurch = d.getChurches()[0]
ProtestantChurch  = d.getChurches()[1]

#testbus
testBus = you.startBusiness("Williamson Shipping LTD")
testFarm = u.Farm("Bill's Farm", Jonestown, (23,23), testBus)
testMill = u.Mill("Bill's Mill", Jonestown, (23,25), testBus)
testBakery = u.Bakery("Bill's Bakery", Jonestown, (25,25), testBus)

#jobs
testFarmer = j.Farmer(10, testBus, testFarm, 40)
testMiller = j.Miller(10, testBus, testMill, 40)
testBaker = j.Baker(10, testBus, testBakery, 40)

#craft orders
testGrain = testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX)
testFlour = testBus.craftOrderManager(testMiller, d.FLOUR_INDEX)
testBread = testBus.craftOrderManager(testBaker, d.BREAD_INDEX)

testGrain.setAmount(50000)
testFlour.setAmount(50000)
testBread.setAmount(50000)

testFarm.DMC[d.GRAIN_INDEX] = 50
testBakery.DMC[d.BREAD_INDEX] = 50
testFarm.addStock(d.GRAIN_INDEX, 10000)
testBakery.addSales(d.BREAD_INDEX, 40)

#harvest orders
harvestOrder = testBus.harvestOrderManager(testFarmer, d.GRAIN_INDEX)
harvestOrder.setAmount(50000)

#transport orders
grainTrans = testBus.transportOrderManager(testFarm.staff.carrier, testFarm, testMill, d.GRAIN_INDEX)
grainTrans.setAmount(500)

flourTrans = testBus.transportOrderManager(testMill.staff.carrier, testMill, testBakery, d.FLOUR_INDEX)
flourTrans.setAmount(500)

#transfer orders
breadFer = testBus.transferOrderManager(testBakery.staff.manager, testBakery, d.BREAD_INDEX)
breadFer.setAmount(500)

# # Main

# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()

model.gui.mainloop()

for unit in testBus.getUnits():
    print(unit.toString())
    print(unit.incubator.toString())

# # cProfile

# model.clock.runDay()
# model.clock.runDay()
# model.clock.runDay()
# cProfile.run("model.clock.runDay()",sort="cumtime")

# print(model.char.knownStores)
# for store in model.char.knownStores:
#     print(store)

# # print(you.muList)
# # # # you.home.output[d.BREAD_INDEX] = 54
# testBakery.output[d.BREAD_INDEX] = 1
# testBakery.output[d.BEER_INDEX] = 50
# testBakery.output[d.CHAIR_INDEX] = 50
# testBakery.price[d.BREAD_INDEX] = 5
# testBakery.price[d.BEER_INDEX] = 5
# testBakery.price[d.CHAIR_INDEX] = 5
# # # you.allMu()
# # # print(you.muList)
# # you.goShopping()
# # you.printThoughts()

# # # you.capital = 0
# print(you.muList)
# print(you.capital, testBus.cash)
# print(you.home.output, testBakery.output)
# print(testBakery.price)
# you.purchase(testBakery)
# you.storeAtHome()
# print(you.capital, testBus.cash)
# print(you.home.output, testBakery.output)
# you.allMu()
# print(you.muList)
# you.printThoughts()