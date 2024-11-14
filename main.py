import random
import copy
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
model.week.machine.set_state('Thursday')

#players
MrMoney = d.getPeople()[0]
MrsMoney = d.getPeople()[1]
you = model.gui.char

CatholicChurch = d.getChurches()[0]
ProtestantChurch  = d.getChurches()[1]

#testbus
testBus = you.startBusiness("Williamson Shipping LTD")
testBus.cash = 1000000

d.addBoss(you)

DEBUG = False
if not DEBUG:
    model.gui.mainloop()
else:
    you.run_day()
    farm = testBus.getUnits()[0]
    mill = testBus.getUnits()[1]
    bakery = testBus.getUnits()[2]
# print(testBus.cash)




# testFarm = u.Farm("Bill's Farm", Jonestown, (23,23), testBus)
# testMill = u.Mill("Bill's Mill", Jonestown, (23,25), testBus)
# testBakery = u.Bakery("Bill's Bakery", Jonestown, (25,25), testBus)

# #jobs
# testFarmer = j.Farmer(10, testBus, testFarm, 6)
# testMiller = j.Miller(10, testBus, testMill, 6)
# testBaker = j.Baker(10, testBus, testBakery, 6)

# for x in range(10):
#     employee = p.People(model, str(x), str(x), 1, Jonestown, you.home, d.getReligions()[0])
#     testFarmer.employees.append(employee)

# testBaker.resetIdlers()
# testBakery.addStock(d.FLOUR_INDEX, 5000)
# testBaker.craft(d.BREAD_INDEX, 540)

# testFarm.incubator.ripe["grain"].append(1000)
# testFarm.incubator.rot_timers["grain"].append(10)

# testFarmer.resetIdlers()
# print(testFarm.toString())
# print(testFarm.incubator.toString())

# testFarm.addStock(d.GRAIN_INDEX, 1000000)

# testFarmer.plant(d.GRAIN_INDEX, 5)
# testFarmer.plant(d.GRAIN_INDEX, 7)
# testFarmer.harvest(d.GRAIN_INDEX)

# print(testFarm.toString())
# print(testFarm.incubator.toString())

# for employee in testFarmer.employees:
#     employee.printThoughts()
# harvestOrder = testBus.harvestOrderManager(testFarmer, d.GRAIN_INDEX)

# testFarm.bigdata.updateSales([8 for i in d.getMaterials()])
# testFarm.bigdata.updateSales([4 for i in d.getMaterials()])
# testFarm.bigdata.updateSales([0 for i in d.getMaterials()])

# testFarm.bigdata.updateFailSales([2 for i in d.getMaterials()])
# testFarm.bigdata.updateFailSales([2 for i in d.getMaterials()])
# testFarm.bigdata.updateFailSales([2 for i in d.getMaterials()])

# testFarm.bigdata.updateTransports([2 for i in d.getMaterials()])
# testFarm.bigdata.updateTransports([2 for i in d.getMaterials()])
# testFarm.bigdata.updateTransports([2 for i in d.getMaterials()])

# testFarm.bigdata.updateFailTransports([2 for i in d.getMaterials()])
# testFarm.bigdata.updateFailTransports([2 for i in d.getMaterials()])
# testFarm.bigdata.updateFailTransports([2 for i in d.getMaterials()])

# print("testFarm avg demand:", testFarm.bigdata.getAvgDemand(d.GRAIN_INDEX))


# for day in range(5):
#     model.clock.runDay()
#     print("order i, amount:", testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX).materialIndex, testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX).amount)
    # print("testFarm avgDemand: ", testFarm.bigdata.getAvgDemand(d.GRAIN_INDEX))
    # print("slots, employees: ", testFarmer.slots, testFarmer.employees)

# print("slots, employees: ", testFarmer.slots, testFarmer.employees)

# order = testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX)
# order.setAmount(50000)
# model.jobPoster.managePositions(testFarmer)

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

# testFarm.toString()
# print(testFarm.incubator.toString())
# print("testFarm avgDemand: ", testFarm.bigdata.getAvgDemand(d.GRAIN_INDEX))
# print("order i, amount:", testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX).materialIndex, testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX).amount)
# print("transfer i, amount: ", testBus.transferOrderManager(testFarm, d.GRAIN_INDEX).materialIndex, testBus.transferOrderManager(testFarm, d.GRAIN_INDEX).amount)
# print("slots, employees: ", testFarmer.slots, testFarmer.employees)
# model.clock.runDay()
# model.clock.runDay()

# print(testBakery.bigdata.getAvgSales(d.BREAD_INDEX))
# model.clock.runDay()
# harvestOrder.setAmount(50000)
# testFarmer.harvest(d.GRAIN_INDEX)
# harvestOrder.execute()

# print(testFarm.toString())
# print(testFarm.incubator.toString())

# testBakery.failSales[d.BREAD_INDEX] = 500

# print("craftOrders: ", testBus.craftOrders)
# for order in testBus.craftOrders:
#     print("Product: ", order.materialIndex)
#     print("Amount: ", order.amount)

# for employee in testFarmer.employees:
#     employee.printThoughts()
# print(model.getDayNum())
# print(testFarmer.idlers)




# testFarm.addFailSales(d.GRAIN_INDEX, 100)
# testBakery.addStock(d.FLOUR_INDEX,1000000)
# for day in range(5):
#     model.clock.runDay()

# print(testBakery.bigdata.getMonth(d.BREAD_INDEX))
# print(testFarm.incubator.toString())


# print("units: ")
# print(testBus.m_unitList)
# print("craftOrders: ")
# for order in testBus.craftOrders:
#     print(order, order.getJob(), order.getJob().getUnit(), order.getProductIndex(), order.amount)
# print("transferOrders: ")
# for order in testBus.transferOrders:
#     print(order, order.getJob(), order.getJob().getUnit(), order.getProductIndex(), order.amount)
# print("transportOrders: ")
# for order in testBus.transportOrders:
#     print(order, order.getJob(), order.getJob().getUnit(), order.getProductIndex(), order.amount, order.unit1, order.unit2)
# print(model.clock.toString())
# print("testMill crafted: ", testMill.crafted)
# print("testBakery crafted: ", testBakery.crafted)
# for customer in testBakery.bigdata.customers[model.getDayNum()]:
#     print(customer)
    
# print("testMill demand: ", testMill.getTotalDemand())
# print("testMill stock, output: ", testMill.stock, testMill.output)
# print("testBakery demand: ", testBakery.getTotalDemand())
# print("testBakery stock, output: ", testBakery.stock, testBakery.output)
# print("Bakers: ", testBaker.getEmployees())

# print("Bakery recent sales: ", testBakery.bigdata.getRecentSales(3))
# print("Bakery recent failSales: ", testBakery.bigdata.getRecentFailSales(3))

# print("testFarm demand: ", testFarm.getTotalDemand())
# print(testFarm.incubator.toString())

# print("testFarm recent sales: ", testFarm.bigdata.getRecentSales(3))
# print("testFarm recent failSales: ", testFarm.bigdata.getRecentFailSales(3))


# #craft orders
# testGrain = testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX)
# testFlour = testBus.craftOrderManager(testMiller, d.FLOUR_INDEX)
# testBread = testBus.craftOrderManager(testBaker, d.BREAD_INDEX)

# testGrain.setAmount(50000)
# testFlour.setAmount(50000)
# testBread.setAmount(50000)

# #stock
# testFarm.addStock(d.GRAIN_INDEX, 10000)
# # testBakery.addStock(d.BREAD_INDEX, 100)

# #harvest orders
# harvestOrder = testBus.harvestOrderManager(testFarmer, d.GRAIN_INDEX)
# harvestOrder.setAmount(50000)

# #transport orders
# # grainTrans = testBus.transportOrderManager(testFarm, testMill, d.GRAIN_INDEX)
# grainTrans = testBus.transportOrderManager(testMill, d.GRAIN_INDEX)
# grainTrans.setAmount(500)

# # flourTrans = testBus.transportOrderManager(testMill, testBakery, d.FLOUR_INDEX)
# flourTrans = testBus.transportOrderManager(testBakery, d.FLOUR_INDEX)
# flourTrans.setAmount(500)

# #transfer orders
# breadFer = testBus.transferOrderManager(testBakery, d.BREAD_INDEX)
# breadFer.setAmount(500)

# print(grainTrans.getStartUnit())
# print(flourTrans.getStartUnit())

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

# model.clock.next_state()
# model.clock.next_state()
# model.clock.next_state()

# print(model.clock.state)

# model.gui.mainloop()
# i = 0
# boss = random.choice(d.bossList)
# while boss == model.char and i < 10:
#     boss = random.choice(d.bossList)
#     i += 1

# print(boss.businesses[0].m_unitList)
# aibakery = boss.businesses[0].m_unitList[1]
# aibakery.toString()
# print(len(boss.businesses[0].m_employees))
# print(you.home.output)
# you.allMu()
# print(you.muList)
# person = random.choice(d.getPeople())
# person.muList = [0 for x in person.muList]
# you.muList = [0 for x in you.muList]
# testBakery.output[d.BREAD_INDEX] = 3.75
# you.purchase(testBakery)

# person.printThoughts()
# you.printThoughts()
# print(model.clock.getDayNum())

# testFarm.toString()
# testMill.toString()
# testBakery.toString()

# for x in testBakery.bigdata.getMonth(d.BREAD_INDEX):
#     print(x)

# for i in range(30):
#     model.clock.runDay()
# model.clock.runDay()
# print(testBakery.toString())
# print(testBakery.dailyCrafted())
# print(testBakery.dailyRevenue())
# model.clock.runDay()
# print(testBakery.toString())
# print(testBakery.dailyCrafted())
# print(testBakery.dailyRevenue())
# model.clock.runDay()
# print(testBakery.toString())
# print(testBakery.dailyCrafted())
# print(testBakery.dailyRevenue())
# model.clock.runDay()
# print(testBakery.toString())
# print(testBakery.dailyCrafted())
# print(testBakery.dailyRevenue())
# print(testBakery.bigdata.sales)

# for unit in testBus.getUnits():
#     print(unit.toString())
#     print(unit.incubator.toString())

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