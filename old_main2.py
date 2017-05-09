import database as d
import people as p
import jobs as j
import unit as u
import business as b
import gameMap as g
import profiles as pr
import generator as gen
import random
from ai import startupAI
from conversation import Convo

#main

#world generator
worldGen = gen.generator()
BraveNewWorld = worldGen.generateWorld(30000, 10, 10)
Jonestown = d.getLocality()[0]
Jonestown.week.machine.set_state('Friday')

#people, unit, business test
JohnDoe = d.peopleList[0]
JaneDoe = d.peopleList[1]
JimSmith = d.peopleList[2]
SusanSmith = d.peopleList[3]
JoeJohnson = d.peopleList[4]
SallyJohnson = d.peopleList[5]

MillersMill = b.Business("Miller's Mill", Jonestown, 1000000)

TheMill = u.Mill("The old mill", Jonestown, (1,1), MillersMill)
MillersWarehouse = u.Warehouse("Miller's Warehouse", Jonestown, (7,3), MillersMill)
Bakery = u.Bakery("Ye Olde Bakery", Jonestown, (7,1), MillersMill)
WheatFarm = u.Farm("Johnson's Wheat Farm", Jonestown, (5,1), MillersMill)

BraveNewWorld.printMap()
Jonestown.printMap()

#jobs test
MillingJob = j.Miller(9000, MillersMill, TheMill, 400)
Transporter = j.Carrier(1, MillersMill, MillersWarehouse, 400)
ManagerJob = j.Manager(MillersMill, Bakery, 400)
BakerJob = j.Baker(9000, MillersMill, Bakery, 400)
FarmerJob = j.Farmer(9000,MillersMill, WheatFarm, 400)

print("Hire JaneDoe MillingJob:", MillersMill.hire(JaneDoe,MillingJob))
MillersMill.fire(JaneDoe)
print("Hire JaneDoe MillingJob (should fail):", MillersMill.hire(JaneDoe,MillingJob))
print("Hire JohnDoe Transporter:", MillersMill.hire(JohnDoe,Transporter))
print("Hire SusanSmith ManagerJob:", MillersMill.hire(SusanSmith,ManagerJob))
print("Hire JimSmith ManagerJob (should fail):", MillersMill.hire(JimSmith,ManagerJob))
print("Hire JimSmith BakerJob:", MillersMill.hire(JimSmith,BakerJob))
print("Hire SallyJohnson BakerJob:", MillersMill.hire(SallyJohnson,BakerJob))
print("Hire JoeJohnson FarmerJob:", MillersMill.hire(JoeJohnson,FarmerJob))
print("MillingJob slots:", MillingJob.getSlots())
print("ManagerJob slots:", ManagerJob.getSlots())
print(JaneDoe.toString())
print(JohnDoe.toString())
print(SusanSmith.toString())
print(JimSmith.toString())

# fill slots
hireIndex = 10
print(MillingJob.getSlots())
while MillingJob.getSlots() > 0:
    randomPerson = d.peopleList[hireIndex]
    MillersMill.hire(randomPerson, MillingJob)
    hireIndex = hireIndex + 1
    # print("Remaining milling job slots:",MillingJob.getSlots())

while BakerJob.getSlots() > 0:
    randomPerson = d.peopleList[hireIndex]
    MillersMill.hire(randomPerson, BakerJob)
    hireIndex = hireIndex + 1
    # print("Remaining baking job slots:",BakerJob.getSlots())

while FarmerJob.getSlots() > 0:
    randomPerson = d.peopleList[hireIndex]
    MillersMill.hire(randomPerson, FarmerJob)
    hireIndex = hireIndex + 1

WheatFarm.addStock(0,1000)
WheatFarm.DMC[0] = 1

#orders
MillersMill.createOrder("work", FarmerJob.plant, [0,3000])
MillersMill.createOrder("work", FarmerJob.harvest, [0])
MillersMill.createOrder("work", MillingJob.craft, [1, 3000])
MillersMill.createOrder("work", BakerJob.craft, [3, 3000])

MillersMill.createOrder("shop", Transporter.transportMats, [WheatFarm, TheMill, 0, 1000])
MillersMill.createOrder("shop", Transporter.transportMats, [TheMill, MillersWarehouse, 1, 3000])
MillersMill.createOrder("shop", Transporter.transportMats, [MillersWarehouse, Bakery, 1, 3000])

MillersMill.createOrder("shop", ManagerJob.transferMats, [TheMill, 1, 1000])
MillersMill.createOrder("shop", ManagerJob.transferMats, [MillersWarehouse, 1, 3000])
MillersMill.createOrder("shop", ManagerJob.transferMats, [Bakery, 3, 3000])

MillersMill.createOrder("rest", ManagerJob.updatePrices, [WheatFarm])
MillersMill.createOrder("rest", ManagerJob.updatePrices, [TheMill])
MillersMill.createOrder("rest", ManagerJob.updatePrices, [MillersWarehouse])
MillersMill.createOrder("rest", ManagerJob.updatePrices, [Bakery])

#profiles
p_Bakery = pr.StoreProfile(Bakery)
p_Bakery.updateLocality(Jonestown)
p_Bakery.updateExperience(10)
p_Bakery.updateLocation(Bakery.getLocation())

p_Bakery.updatePrices([1,1,1,1], Jonestown.clock.getDayNum())

JaneDoe.knownStores.append(p_Bakery)

#conversation
JohnDoe.peopleManager(SusanSmith)

JaneDoe.knownStores[0].updatePrices(JaneDoe.knownStores[0].getPrices(), 5)
print(d.unitList[15])
JohnDoe.knownPeople[0].updateJob(SusanSmith.getJob(), 5)
print(JohnDoe.knownPeople[0].name)

Convo.beginConversation(JaneDoe, JohnDoe)
print("convoState", Convo.state)
print(JaneDoe.thoughts)

#profile tests
print("real names: ", JimSmith.name, SallyJohnson.name)
print("SallyJohnson profile:", SallyJohnson.myProfile)

print("JimSmith known people:",JimSmith.knownPeople)
for person in JimSmith.knownPeople:
    print(person.name, person.job)
print("SallyJohnson known people:",SallyJohnson.knownPeople)
for person in SallyJohnson.knownPeople:
    print(person.name, person.job)

print("JimSmith known people:",JimSmith.knownPeople)
for person in JimSmith.knownPeople:
    print(person.name, person.job)
print("SallyJohnson known people:",SallyJohnson.knownPeople)
for person in SallyJohnson.knownPeople:
    print(person.name, person.job)

Jonestown.clock.runDay()
Jonestown.clock.runDay()
Jonestown.clock.runDay()

print(JaneDoe.capital)
JaneDoe.printThoughts()
JohnDoe.printThoughts()
BakerJob.getEmployees()[80].printThoughts()
print(JaneDoe.home.output)

for store in JohnDoe.knownStores:
    print(store.name, store.avgPrices, store.familiarity, store.experience)

print("Bakery prices",Bakery.getPrice())

#AI
print("WheatFarm prices",WheatFarm.price)
print("WheatFarm sales",WheatFarm.sales)
print("WheatFarm output",WheatFarm.output)
print("WheatFarm growing",WheatFarm.growing)
print("WheatFarm laborTotal",WheatFarm.laborTotal)
print("WheatFarm employees",FarmerJob.getEmployees())
print("WheatFarm DMC", WheatFarm.DMC)

JohnDoe.manuManager(TheMill)
# startupAI.whatToBuild(JohnDoe)