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

import orders

#main

model = Model()
Jonestown = d.getLocality()[0]
model.week.machine.set_state('Friday')

#players
MrMoney = d.getPeople()[0]
MrsMoney = d.getPeople()[1]
yourHome = u.House(Jonestown, (3,5))
you = model.gui.char
you.addCapital(10000000000)

#businesses
model.builder.newBusiness(you)
MillersMill = you.businesses[0]
# bus2 = you.startBusiness("Mark's Mercenary Services", 1000000)
# bus3 = you.startBusiness("Stalwart Shoes", 100000)

pMrMoney = you.peopleManager(MrMoney)
pMrMoney.updateMuList(MrMoney.getMuList(), Jonestown.getDayNum())
pMrsMoney = you.peopleManager(MrsMoney)
pMrsMoney.updateMuList(MrsMoney.getMuList(), Jonestown.getDayNum())

# i_build = model.startupAI.whatToBuild(you)
# model.builder.buildChain(MillersMill, i_build)

#units
MillersMillUnits = MillersMill.getUnits()
WheatFarm = MillersMillUnits[0]
TheMill = MillersMillUnits[1]
# Bakery = MillersMillUnits[2]

CatholicChurch = d.getChurches()[0]
ProtestantChurch  = d.getChurches()[1]

# #jobs 
ManagerJob = j.Manager(MillersMill, WheatFarm, 40)
TransportJob = j.Carrier(1, MillersMill, WheatFarm, 40)
FarmerJob = you.getBusinesses()[0].getJobs()[0]
MillingJob = you.getBusinesses()[0].getCraftingJobs()[0]
# BakerJob = you.getBusinesses()[0].getCraftingJobs()[1] 

PriestJob = j.Priest(1, CatholicChurch.getBusiness(), CatholicChurch, 40)
MinisterJob = j.Priest(1, ProtestantChurch.getBusiness(), ProtestantChurch, 40)

print("PriestJob filled: ", model.hirer.jobApplication(d.getPeople()[2], PriestJob))
print("MinisterJob filled: ", model.hirer.jobApplication(d.getPeople()[3], MinisterJob))

# farmPrices = orders.pricingOrder(MillersMill, ManagerJob, WheatFarm)
# MillersMill.pricingOrders.append(farmPrices)

# wheatTransport = orders.transportOrder(MillersMill, TransportJob, WheatFarm, TheMill, 0, 100000)
# MillersMill.transportOrders.append(wheatTransport)
# MillersMill.transportOrderManager(TransportJob, WheatFarm, TheMill, 0)

# transferFlour = orders.transferOrder(MillersMill, ManagerJob, TheMill, 1, 50000)
# MillersMill.transferOrders.append(transferFlour)

# millPrices = orders.pricingOrder(MillersMill, ManagerJob, TheMill)
# MillersMill.pricingOrders.append(millPrices)

# flourTransport = orders.transportOrder(MillersMill, TransportJob, TheMill, Bakery, 1, 50000)
# MillersMill.transportOrders.append(flourTransport)

# transferBread = orders.transferOrder(MillersMill, ManagerJob, Bakery, 3, 25000)
# MillersMill.transferOrders.append(transferBread)

# bakeryPrices = orders.pricingOrder(MillersMill, ManagerJob, Bakery)
# MillersMill.pricingOrders.append(bakeryPrices)

#misc
# WheatFarm.sales = [1000,0,0,0]
WheatFarm.addStock(d.WOOD_INDEX,100000)
# WheatFarm.DMC[0] = 1

# TheMill.addStock(d.WOOD_INDEX,1000)
# TheMill.DMC[0] = 1

# Bakery.addStock(1,10000)
# Bakery.DMC[1] = 1

bossNumber = 0
peopleList = d.getPeople()
while bossNumber < 100:
    boss = peopleList[bossNumber]
    model.builder.newBusiness(boss)
    d.bossList.append(boss)

    bossNumber += 1

model.gui.mainloop()
# friend = you.knownPeople[15].person
# friend.printThoughts()
# print(friend.capital)
# print(friend.home.output)

employee = WheatFarm.jobList[0].employees[0]
employee.printThoughts()
print("Employee cash:", employee.capital)

print("harvestOrders: ", MillersMill.harvestOrders)
print("craftOrders: ", MillersMill.craftOrders)
print("transferOrder: ", MillersMill.transferOrders)

for order in MillersMill.harvestOrders:
    print(order.getJob().jobType)

for order in MillersMill.craftOrders:
    print(order.getJob().jobType)
    print(order.getProductIndex())
    print(order.amount)

for order in MillersMill.transferOrders:
    print(order.getJob().jobType)
    print(order.getUnit())
    print(order.getProductIndex())
    print(order.amount)

WheatFarm.toString()