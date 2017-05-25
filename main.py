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


testBus = you.startBusiness("Bill's Mill", 3000)
testMill = u.Bakery("Bill's Bakery", Jonestown, (21,21), testBus)

testManager = j.Manager(testBus, testMill, 40)
testTransfer = testBus.transferOrderManager(testManager, testMill, d.BREAD_INDEX)
testTransfer.setAmount(400)

testJob = j.Baker(10, testBus, testMill, 40)

testOrder = testBus.craftOrderManager(testJob, d.BREAD_INDEX)
testOrder.setAmount(400)

testMill.addSales(d.BREAD_INDEX, 40)
testMill.DMC[d.FLOUR_INDEX] = 100
testMill.addStock(d.FLOUR_INDEX, 5000)

testPricing = o.pricingOrder(testBus, testManager, testMill)
testBus.pricingOrders.append(testPricing)

model.gui.mainloop()

Jonestown.printMap()

print(testMill.incubator.toString())
print(testMill.toString())