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

            i = random.randrange(len(firstNameList))
            firstname = firstNameList[i]

            j = random.randrange(len(lastNameList))
            lastname = lastNameList[j]

            # gennedName = firstName + " " + lastName

            #home            
            k = (count // 2)
            home = houseList[k]

            #religion
            if count < (p_quantity/2):
                religion = religionList[0]
            else:
                religion = religionList[1]

            #gen
            gennedPerson = p.People(self.model, firstname, lastname, gender, 18, locality, home, [1,1,1,1,1,1,1,1,1,1], religion)
            gennedPerson.addCapital(100)

            #spouses
            if (count % 2 == 1):
                spouse = d.getPeople()[-2]
                self.generateSpouse(gennedPerson, spouse)
            
            # church = religion.getBusinesses()[0].getUnits()[0]
            # gennedPerson.unitManager(church)
            # gennedPerson.newChurch(church)

    def generateSpouse(self, wife, husband):
        husband.setSpouse(wife)
        wife.setSpouse(husband)

    def generateReligions(self, locality):
        Catholic = rel.Catholicism()
        Protestant = rel.Protestantism()

        localCatholic = bu.Business([], "Catholic", locality, 10000000)
        localProtestant = bu.Business([], "Protestant", locality, 100000000)

        Catholic.addBusiness(localCatholic)
        Protestant.addBusiness(localProtestant)

        religionList = [Catholic, Protestant]
        return religionList

    #people must be even int because marriages
    #we only generate a single locality- don't ask
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

        return gennedWorld

    #makes are called by model after worldgen completes

    def makeFriends(self):
        peopleList = d.getPeople()
        for person in peopleList:
            for count in range(20):
                i = random.randrange(len(peopleList))
                friend = peopleList[i]
                friendProfile = person.peopleManager(friend)
                friendProfile.updateMuList(friend.getMuList(), person.locality.getDayNum())
                personProfile = friend.peopleManager(person)
                personProfile.updateMuList(person.getMuList(), person.locality.getDayNum())

    #just gives money- actual boss stuff handled in clock and people
    def makeBosses(self):
        peopleList = d.getPeople()
        for i in range(100):
            boss = random.choice(peopleList)
            if boss.capital < 10000:
                boss.capital += 10000

    def makeChurches(self, locality):
        peopleList = d.getPeople()
        perChurch = 30
        churchNum = math.floor(len(peopleList) / perChurch)
        religions = d.getReligions()
        religionNum = len(d.getReligions())

        if churchNum < 1:
            churchNum = 1

        for religion in religions:
            churchPer = math.ceil(churchNum / religionNum)
            business = religion.getLocalBusiness(locality)
            
            for i in range(churchPer):
                churchName = random.choice(religion.churchNames)
                location = locality.find_property()
                newChurch = u.Church(churchName, locality, location, business, religion)
                locality.claim_node(location, newChurch)

    def assignChurches(self):
        peopleList = d.getPeople()

        for person in peopleList:
            religion = person.getReligion()
            business = religion.getLocalBusiness(person.getLocality())
            church = random.choice(business.getUnits())
            person.unitManager(church)
            person.newChurch(church)