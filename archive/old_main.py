import database as d
import people as p
import jobs as j
import unit as u
import business as b
import gameMap as g
import profiles as pr
import generator as gen

import pickle
import sys

#main

#world generator
worldGen = gen.generator()
BraveNewWorld = worldGen.generateWorld(30, 3, 3)
BraveNewWorld.printMap()
Jonestown = d.getLocality()[0]

#people, unit, business test
JohnDoe = d.peopleList[0]
JaneDoe = d.peopleList[1]
SusanSmith = d.peopleList[2]

MillersMill = b.Business("Miller's Mill", 30)

TheMill = u.Mill("The old mill", Jonestown, (1,1), MillersMill)
MillersWarehouse = u.Warehouse("Miller's Warehouse", Jonestown, (7,3), MillersMill)
Bakery = u.Market("Ye Olde Bakery", Jonestown, (7,1), MillersMill)
Deli = u.Market("Ye Delicious Deli", Jonestown, (1,3), MillersMill)

MillingJob = j.Miller(10, MillersMill, TheMill)
Transporter = j.Carrier(1, MillersMill, MillersWarehouse)
ManagerJob = j.Manager(1, MillersMill, MillersWarehouse)

BraveNewWorld.printMap()
Jonestown.printMap()

#jobs test
print("Hire JaneDoe MillingJob:", MillersMill.hire(JaneDoe,MillingJob))
print("Hire JohnDoe Transporter:", MillersMill.hire(JohnDoe,Transporter))
print("Hire JaneDoe MillingJob:", MillersMill.hire(JaneDoe,MillingJob))
print("Hire SusanSmith ManagerJob:", MillersMill.hire(SusanSmith,ManagerJob))
print("MillingJob slots:", MillingJob.getSlots())
print(JaneDoe.toString())
print(JohnDoe.toString())
print(SusanSmith.toString())

print("TheMill initial grain stock:", TheMill.getStock(0))
TheMill.addStock(0,10)
print("TheMill final grain stock:", TheMill.getStock(0))

print("Grain:", TheMill.getStock(0))
print("Flour:", TheMill.getStock(1))
print(MillingJob.grind(3))
print("Grain:", TheMill.getStock(0))
print("Flour:", TheMill.getStock(1))

print("MillingJob final employees:", MillingJob.getEmployees())

print("TheMill initial output:", TheMill.output)
ManagerJob.transferMats(TheMill,1,3)

print("TheMill middle output:", TheMill.output)

Transporter.transportMats(TheMill, MillersWarehouse, 1, 2)

print("TheMill final output:", TheMill.output)
print("MillersWarehouse stock:", MillersWarehouse.stock)

#orders test
print("TheMill stock:", TheMill.stock)
MillersMill.createOrder(MillingJob.grind, [2])
MillersMill.orders[0].execute()
print("TheMill stock:", TheMill.stock)

#mu test
JaneDoe.home.stock = [1,2,0,1]
print("JaneDoe home stock:", JaneDoe.home.getAllStock())
JaneDoe.marginalUtility()
print("JaneDoe mu:",JaneDoe.getmuList())

#store choice test
p_Bakery = pr.StoreProfile(Bakery)
p_Bakery.updateLocality(Jonestown)
p_Bakery.updateFamiliarity(5)
p_Bakery.updateExperience(1)
p_Bakery.updateLocation(Bakery.getLocation())
p_Bakery.updatePrices([1,1,1,1])

p_Deli = pr.StoreProfile(Deli)
p_Deli.updateLocality(Jonestown)
p_Deli.updateFamiliarity(5)
p_Deli.updateExperience(10)
p_Deli.updateLocation(Deli.getLocation())
p_Deli.updatePrices([1,1,1,1])

JaneDoe.knownStores.append(p_Bakery)
JaneDoe.knownStores.append(p_Deli)
print("JaneDoe chooses to shop at:",JaneDoe.chooseStore()[0].name)

#pricegen test
Bakery.output = [1,0,1,5]
Bakery.capital = [6,1,1,1]
Bakery.price = [1,1,1,1]
Bakery.sales = [1,0,10,10]

Deli.output = [1,0,1,5]
Deli.capital = [6,1,1,1]
Deli.price = [1,1,1,1]
Deli.sales = [1,0,10,10]

print("Bakery initial prices:",Bakery.price)
Bakery.priceGen()
print("Bakery final prices:",Bakery.price)

#purchase test
JaneDoe.capital = 100
print("JaneDoe initial capital:",JaneDoe.capital)
print("Bakery initial capital:",Bakery.money)
JaneDoe.purchase(Bakery)
print("Bakery final capital:",Bakery.money)
print("JaneDoe final capital:",JaneDoe.capital)

print("JaneDoe inventory:",JaneDoe.getInventory())
print("Bakery final output:",Bakery.output)

#FSM test
print("Time:",Jonestown.clock.state)
print("Day of week:",Jonestown.week.state)
Jonestown.clock.next_state()
print("Time:",Jonestown.clock.state)
print("Day of week:",Jonestown.week.state)
print(JaneDoe.state)
JaneDoe.wake_up()
print(JaneDoe.state)
JaneDoe.work_end()
print(JaneDoe.state)
JaneDoe.wind_down()
print(JaneDoe.state)
JaneDoe.bedtime()
print(JaneDoe.state)


#write to file test
# output = open("./peopleDatabase.txt", "wb")
# pickle.dump(JaneDoe, output)

# ourFile = open("./peopleDatabase.txt", "rb")
# JanetteDoe = pickle.load(ourFile)
# print(JanetteDoe.chooseStore()[0].name)