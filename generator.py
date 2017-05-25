import database as d
import gameMap as g
import business as bu
import religion as rel
import unit as u
import people as p
import profiles as pr
import random
import math

class generator(object):

    def __init__(self, model):
        self.model = model

    def generateHouses(self, h_quantity, locality):
        #locations
        x = -2
        y = 0
        length = locality.getWidth()
        houseList = []

        for count in range(h_quantity):
            x = (x + 2) % length
            y = 2 * ((count*2) // length)
            location = (x,y)
            gennedHouse = u.House(locality, location)
            locality.claim_node(location, gennedHouse)
            houseList.append(gennedHouse)

        return houseList

    def generateLocality(self, l_location):
        #locality size, name static for now
        gennedLocality = g.Locality(self.model, l_location,150,150,"Jonestown")
        return gennedLocality

    def generatePeople(self, p_quantity, locality, houseList, religionList):

        lastNameList = d.getLastNameList()

        for count in range(p_quantity):
            
            #gender
            if (count % 2 == 0):
                gender = 0
            else:
                gender = 1

            #name
            firstNameList = d.getFirstNameList(gender)

            i_firstName = random.randrange(len(firstNameList))
            firstName = firstNameList[i_firstName]

            i_lastName = random.randrange(len(lastNameList))
            lastName = lastNameList[i_lastName]

            gennedName = firstName + " " + lastName

            #home            
            i_home = (count // 2)
            home = houseList[i_home]

            #religion
            if count < (p_quantity/2):
                religion = religionList[0]
            else:
                religion = religionList[1]

            #gen
            gennedPerson = p.People(self.model, gennedName, gender, 18, locality, home,[1,1,1,1,1,1,1,1,1,1], religion)
            gennedPerson.addCapital(100)
            
            church = religion.getBusinesses()[0].getUnits()[0]
            gennedPerson.unitManager(church)
            gennedPerson.newChurch(church)

    def generateStore(self, locality):
        #NewWorldDefaults are starting businesses for the world. They have no owner and will run out of supplies and go bankrupt.
        NewWorldDefaults = bu.Business(None, "New World Starting Stores", locality, 200)
        NewWorldGeneralStore = u.Bakery("New World General Store", locality, (1,3), NewWorldDefaults)
        dayNum = locality.clock.getDayNum()
        
        for i in range(len(NewWorldGeneralStore.output)):
            NewWorldGeneralStore.addOutput(i,50)
            NewWorldGeneralStore.price[i] = 1

        for person in d.getPeople():
            p_NewWorldGS = pr.StoreProfile(NewWorldGeneralStore)
            person.knownStores.append(p_NewWorldGS)
            p_NewWorldGS.updateLocality(locality)
            p_NewWorldGS.updateLocation(NewWorldGeneralStore.getLocation())
            p_NewWorldGS.updatePrices(NewWorldGeneralStore.getPrice(), dayNum)
            p_NewWorldGS.updateExperience(.0000000001)

    def generateReligions(self, locality):
        Catholic = rel.Catholicism()
        Protestant = rel.Protestantism()

        localCatholic = bu.Business([], "Catholic", locality, 10000000)
        localProtestant = bu.Business([], "Protestant", locality, 100000000)

        Catholic.addBusiness(localCatholic)
        Protestant.addBusiness(localProtestant)

        cChurch = u.Church("Blessed Mother Cathedral", locality, (0,1), localCatholic, Catholic)
        pChurch = u.Church("Martin Luther Prayer Hall", locality, (1,1), localProtestant, Protestant)

        religionList = [Catholic, Protestant]
        return religionList

    def makeFriends(self):
        peopleList = d.getPeople()
        for person in peopleList:
            for count in range(10):
                i = random.randrange(len(peopleList))
                friend = peopleList[i]
                friendProfile = person.peopleManager(friend)
                friendProfile.updateMuList(friend.getMuList(), person.locality.getDayNum())
                personProfile = friend.peopleManager(person)
                personProfile.updateMuList(person.getMuList(), person.locality.getDayNum())

    #people must be even int
    #for now we only generate a single locality
    def generateWorld(self, p_quantity, w_width, w_height):
        peopleList = []

        #need even number of people for marriages
        if p_quantity % 2 != 0.0:
            print("Please choose an even number of people for your world.")
            return False

        #world
        gennedWorld = g.World(w_width, w_height)

        #locality
        l_location = (random.randrange(w_width), random.randrange(w_height))
        gennedLocality = self.generateLocality(l_location)

        #houses, people, store
        h_quantity = int(p_quantity/2)
        houseList = self.generateHouses(h_quantity, gennedLocality)
        religions = self.generateReligions(gennedLocality)
        self.generatePeople(p_quantity, gennedLocality, houseList, religions)
        # self.makeFriends()

        return gennedWorld