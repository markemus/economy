import database as d
import people as p
import jobs as j
import unit as u
import business as b
import gameMap as g
import profiles as pr
import generator as gen
import ai
import random
from conversation import Convo
from gui import gui
from model import Model

import orders as o

#main

model = Model()
Jonestown = d.getLocality()[0]
model.week.machine.set_state('Friday')

#players
MrMoney = d.getPeople()[0]
MrsMoney = d.getPeople()[1]
yourHome = u.House(Jonestown, (3,5))
you = model.gui.char
model.gui.char.name = "Brian Jones"
you.addCapital(10000)

CatholicChurch = d.getChurches()[0]
ProtestantChurch  = d.getChurches()[1]

bossNumber = 0
peopleList = d.getPeople()
while bossNumber < 100:
    boss = peopleList[bossNumber]
    model.builder.newBusiness(boss)
    d.bossList.append(boss)

    bossNumber += 1
if you in d.bossList:
    d.bossList.remove(you)

#testbus
testBus = you.startBusiness("Williamson Shipping LTD", 3000)
testFarm = u.Farm("Bill's Farm", Jonestown, (23,23), testBus)
testMill = u.Mill("Bill's Mill", Jonestown, (23,25), testBus)
testBakery = u.Bakery("Bill's Bakery", Jonestown, (25,25), testBus)

testFarmer = j.Farmer(10, testBus, testFarm, 40)
testMiller = j.Miller(10, testBus, testMill, 40)
testBaker = j.Baker(10, testBus, testBakery, 40)

# testGrain = testBus.craftOrderManager(testFarmer, d.GRAIN_INDEX)
testFlour = testBus.craftOrderManager(testMiller, d.FLOUR_INDEX)
testBread = testBus.craftOrderManager(testBaker, d.BREAD_INDEX)

# testGrain.setAmount(50000)
testFlour.setAmount(50000)
testBread.setAmount(50000)

# testFarm.addSales(d.GRAIN_INDEX, 40)
testFarm.DMC[d.GRAIN_INDEX] = 50
testFarm.addStock(d.GRAIN_INDEX, 100)

# for mat in range(len(d.getMaterials())):
#     testMill.addStock(mat, 5000)

model.gui.mainloop()

# Jonestown.printMap()

# print(testMill.incubator.toString())

for unit in testBus.getUnits():
    print(unit.toString())
    print(unit.incubator.toString())