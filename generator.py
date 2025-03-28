import random
import math

import numpy as np

import database as d
import gameMap as g
import business as bu
import religion as rel
import unit as u
import people as p


class generator(object):
    def __init__(self, model):
        self.model = model

    # TODO-DONE houses should be generated in zoned areas only
    def generateHouses(self, h_quantity, locality):
        # get locations
        houseList = []
        zmap = locality.getZoningMap()
        house_tiles = np.argwhere(zmap=="h")
        np.random.shuffle(house_tiles)

        for location in house_tiles[:h_quantity]:
            gennedHouse = u.House(locality, location)
            locality.claim_node(location, gennedHouse)
            houseList.append(gennedHouse)

        return houseList

    def generateLocality(self, l_location):
        # locality size, name static for now
        # TODO-DONE 100x100
        gennedLocality = g.Locality(self.model, l_location, 100, 100, "Jonestown")
        return gennedLocality

    # TODO not everyone should get their own house. Make 50% single living with parents (varying size families).
    def generatePeople(self, p_quantity, locality, houseList, religionList):
        lastNameList = d.getLastNameList()

        for count in range(p_quantity):
            # gender
            if (count % 2 == 0):
                gender = 0
            else:
                gender = 1

            # name
            firstNameList = d.getFirstNameList(gender)

            i = random.randrange(len(firstNameList))
            firstname = firstNameList[i]

            j = random.randrange(len(lastNameList))
            lastname = lastNameList[j]

            # TODO unmarried people should start in their parents' home (need parents)
            # home
            k = (count // 2)
            home = houseList[k]

            # religion
            if count < (p_quantity/2):
                religion = religionList[0]
            else:
                religion = religionList[1]

            # gen
            gennedPerson = p.People(self.model, firstname, lastname, gender, locality, home, religion)
            gennedPerson.addCapital(100)
            gennedPerson.home.addTenant(gennedPerson)

    # TODO add holidays.
    # TODO protestant churches should not be a single business, catholic should.
    def generateReligions(self, locality):
        Catholic = rel.Catholicism()
        Protestant = rel.Protestantism()

        localCatholic = bu.Business([], "Catholic", locality, 10000000)
        localProtestant = bu.Business([], "Protestant", locality, 100000000)

        Catholic.addBusiness(localCatholic)
        Protestant.addBusiness(localProtestant)

        religionList = [Catholic, Protestant]
        return religionList

    # TODO more chaotic map generation. How to organize houses and store locations? Churches should
    #  be scattered around. Stores should be near owner's house? Start with neighbors, not friends.
    # people must be even int because marriages
    # we only generate a single locality- don't ask
    def generateWorld(self, p_quantity, w_width, w_height):
        peopleList = []

        # need even number of people for marriages
        if p_quantity % 2 != 0:
            print("Please choose an even number of people for your world.")
            return False

        # world
        gennedWorld = g.World(w_width, w_height)

        # locality
        l_location = (random.randrange(w_width), random.randrange(w_height))
        gennedLocality = self.generateLocality(l_location)

        # TODO generate from center, not corner. Houses should cluster together with open areas for markets.
        # TODO farms on the outskirts. Zoning?
        # houses, people, store
        h_quantity = p_quantity // 2
        houseList = self.generateHouses(h_quantity, gennedLocality)
        religions = self.generateReligions(gennedLocality)
        self.generatePeople(p_quantity, gennedLocality, houseList, religions)

        return gennedWorld

    # makes are called by model after worldgen completes
    # TODO-DONE Spouses should have 10 opinion of one another.
    def makeSpouses(self):
        peopleList = d.getPeople()
        
        i = 0

        for index in range((len(peopleList) // 2)):
            wife = peopleList[i]
            husband = peopleList[i + 1]
            wife.setSpouse(husband)
            husband.setSpouse(wife)

            # Create profiles and update opinion
            husband.peopleManager(wife).updateOpinion(10)
            wife.peopleManager(husband).updateOpinion(10)

            # Share home
            # TODO people should start in their parents home and move in together to a new home when married.
            wife.home.removeTenant(wife)
            wife.setHome(husband.getHome())
            wife.home.addTenant(wife)

            # Update basic info
            husband.peopleManager(wife).updateBirthday(wife.birthday)
            husband.peopleManager(wife).updateHouse(wife.getHome(), self.model.getDayNum())
            husband.peopleManager(husband).updateFamily(spouse=(husband.peopleManager(wife), self.model.getDayNum()))
            husband.peopleManager(wife).updateFamily(spouse=(husband.peopleManager(husband), self.model.getDayNum()))
            husband.peopleManager(wife).updateMuList(wife.getMuList(), wife.locality.getDayNum())

            wife.peopleManager(husband).updateBirthday(husband.birthday)
            wife.peopleManager(husband).updateFamily(spouse=(wife.peopleManager(wife), self.model.getDayNum()))
            wife.peopleManager(wife).updateFamily(spouse=(wife.peopleManager(husband), self.model.getDayNum()))
            wife.peopleManager(husband).updateHouse(husband.getHome(), self.model.getDayNum())
            wife.peopleManager(husband).updateMuList(husband.getMuList(), husband.locality.getDayNum())

            i += 2

    # TODO-DONE friends should start out with 5 opinion of each other.
    def makeFriends(self):
        peopleList = d.getPeople()
        for person in peopleList:
            for count in range(3):
                i = random.randrange(len(peopleList))
                friend = peopleList[i]
                friendProfile = person.peopleManager(friend)
                friendProfile.updateMuList(friend.getMuList(), person.locality.getDayNum())
                friend.peopleManager(person).updateOpinion(5)

                personProfile = friend.peopleManager(person)
                personProfile.updateMuList(person.getMuList(), person.locality.getDayNum())
                person.peopleManager(friend).updateOpinion(5)

    # TODO bosses should start with far less money (maybe just a loan from a bank instead)
    # just gives money- actual boss stuff handled in clock and people
    def makeBosses(self):
        peopleList = d.getPeople()
        for i in range(100):
            boss = random.choice(peopleList)
            if boss.capital < 1000000:
                boss.capital += 1000000

    # TODO-DONE there are currently far too many churches. They should be spaced better too instead of clustering in NW.
    # TODO-DONE churches should use business zones.
    def makeChurches(self, locality):
        peopleList = d.getPeople()
        perChurch = 90
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
                location = locality.find_property(zone="b")
                newChurch = u.Church(churchName, locality, location, business, religion)
                locality.claim_node(location, newChurch)

    # TODO people should shop around for churches just like businesses. But they should settle on one?
    # TODO people should be assigned to nearby churches.
    def assignChurches(self):
        peopleList = d.getPeople()

        for person in peopleList:
            religion = person.getReligion()
            business = religion.getLocalBusiness(person.getLocality())
            # Churches will have more or fewer members by chance.
            church = random.choice(business.getUnits())
            person.unitManager(church)
            person.newChurch(church)
