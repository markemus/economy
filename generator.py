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

    def generateLocality(self, l_location):
        # locality size, name static for now
        gennedLocality = g.Locality(self.model, l_location, 100, 100, "Jonestown")
        return gennedLocality

    def generatePeople(self, p_quantity, locality, religionList):
        lastNameList = d.getLastNameList()

        # Create families
        while p_quantity > len(d.peopleList):
            family_name = random.choice(lastNameList)
            family_religion = random.choice(religionList)

            n_children = round(np.random.default_rng().normal(loc=3, scale=3))
            n_children = min(p_quantity - len(d.peopleList) - 2, n_children)
            n_children = max(0, n_children)

            home_location = locality.find_property(zone="h")
            family_home = u.House(locality, home_location)
            locality.claim_node(home_location, family_home)

            # Parents
            father_name = random.choice(d.getFirstNameList(gender=0))
            father = p.People(self.model, father_name, family_name, 0, locality, family_home, family_religion)
            father.birthday = self.model.calendar.sample_date(year=self.model.calendar.year-random.randint(35, 45))
            family_home.addTenant(father)
            father.addCapital(100)

            mother_name = random.choice(d.getFirstNameList(gender=1))
            mother = p.People(self.model, mother_name, family_name, 1, locality, family_home, family_religion)
            mother.birthday = self.model.calendar.sample_date(year=self.model.calendar.year - random.randint(30, 40))
            family_home.addTenant(mother)
            mother.addCapital(100)

            mother.setSpouse(father)
            father.setSpouse(mother)

            # Children
            # TODO-DONE birthdays and ages
            child_list = []
            for i in range(n_children):
                gender = random.choice([0, 1])
                child_name = random.choice(d.getFirstNameList(gender=gender))
                child = p.People(self.model, child_name, family_name, gender, locality, family_home, family_religion)
                child.birthday = self.model.calendar.sample_date(year=self.model.calendar.year - random.randint(15, 23))
                family_home.addTenant(child)
                child.addCapital(100)
                child_list.append(child)

            for child in child_list:
                other_children = child_list.copy()
                other_children.remove(child)

                child.peopleManager(father).updateFamily(spouse=(child.peopleManager(mother), self.model.getDayNum()), children=(*[child.peopleManager(sibling) for sibling in other_children], self.model.getDayNum()))
                child.peopleManager(mother).updateFamily(spouse=(child.peopleManager(father), self.model.getDayNum()), children=(*[child.peopleManager(sibling) for sibling in other_children], self.model.getDayNum()))
                child.peopleManager(child).updateFamily(father=(child.peopleManager(father), self.model.getDayNum()), mother=(child.peopleManager(mother), self.model.getDayNum()), siblings=(*[child.peopleManager(sibling) for sibling in other_children], self.model.getDayNum()))

                child.peopleManager(father).updateBirthday(father.birthday)
                child.peopleManager(mother).updateBirthday(mother.birthday)
                child.peopleManager(father).updateHouse(father.getHome(), self.model.getDayNum())
                child.peopleManager(mother).updateHouse(mother.getHome(), self.model.getDayNum())

                child.peopleManager(father).updateMuList(father.getMuList(), mother.locality.getDayNum())
                child.peopleManager(mother).updateMuList(mother.getMuList(), mother.locality.getDayNum())

                # print(child.peopleManager(father).getFamilyList())
                # print([x.name for x in child.peopleManager(child).getFamilyList()])

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

    # TODO-DONE more chaotic map generation. How to organize houses and store locations?
    # TODO-DONE Churches should be scattered around.
    # TODO Stores should be near owner's house?
    # TODO-DONE Start with neighbors, not friends.
    # people must be even int because marriages
    # we only generate a single locality- don't ask
    def generateWorld(self, p_quantity, w_width, w_height):
        # world
        gennedWorld = g.World(w_width, w_height)

        # locality
        l_location = (random.randrange(w_width), random.randrange(w_height))
        gennedLocality = self.generateLocality(l_location)

        # TODO-DONE farms on the outskirts. Zoning?
        religions = self.generateReligions(gennedLocality)
        self.generatePeople(p_quantity, gennedLocality, religions)

        return gennedWorld

    # TODO-DONE replace friends with neighbors
    def makeNeighbors(self):
        peopleList = d.getPeople()
        for person in peopleList:
            houses = d.getHouses().copy()
            houses.sort(key=lambda x: person.pyth(x)[0])
            dayNum = person.locality.getDayNum()

            for count in range(random.randint(2, 5)):
                neighbor = random.choice(houses[count].tenants)
                neighborProfile = person.peopleManager(neighbor)
                neighborProfile.updateMuList(neighbor.getMuList(), dayNum)
                neighborProfile.updateOpinion(5)
                neighborProfile.updateBirthday(neighbor.birthday)
                neighborProfile.updateHouse(neighbor.home, dayNum)

                personProfile = neighbor.peopleManager(person)
                personProfile.updateOpinion(5)
                personProfile.updateBirthday(person.birthday)
                personProfile.updateMuList(person.getMuList(), dayNum)
                personProfile.updateHouse(person.home, dayNum)

    # TODO bosses should start with far less money (maybe just a loan from a bank instead)
    # just gives money- actual boss stuff handled in clock and people
    def makeBosses(self):
        peopleList = d.getPeople()
        for i in range(10):
            boss = random.choice(peopleList)
            if boss.capital < 1000000:
                boss.capital += 1000000

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
    # TODO-DONE people should be assigned to nearby churches.
    def assignChurches(self):
        peopleList = d.getPeople()

        for person in peopleList:
            religion = person.getReligion()
            business = religion.getLocalBusiness(person.getLocality())
            # People go to the nearest church at game start.
            all_churches = business.getUnits()
            church = min(all_churches, key=lambda church: person.pyth(church)[0])
            person.unitManager(church)
            person.newChurch(church)
