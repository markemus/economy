import math
import random
import copy

import database as d
from conversation import Convo
from profiles import PersonProfile


# TODO personalities- research shopping types.
# TODO Advertisements- should target particular personalities. IE build a brand.
# TODO surveys- target store customers (yours) or a geographical area.
# TODO surveys and ads should require a manager
# TODO check- prioritize purchases using marginal utility.
class People:
    firstname = "John"
    lastname = "Doe"
    # 0 are men, 1 are women
    gender = 0
    age = 0
    # a localMap
    locality = None
    # a Unit in homeTown
    home = None
    # each index represents a particular skill- shoemaking, or lumberjacking, etc.
    # skills = [0 for i in d.getMaterials()]
    job = None
    salary = 0
    capital = 0
    spouse = None
    church = None

    def __init__(self, model, firstname, lastname, theirGender, theirHometown, theirHome, theirReligion):
        d.addPeople(self)
        self.model = model
        self.firstname = firstname
        self.lastname = lastname
        self.gender = theirGender
        self.age = 0
        self.birthday = self.model.calendar.date()
        self.locality = theirHometown
        self.home = theirHome
        self.location = theirHome.location
        # self.skills = theirSkills
        self.religion = theirReligion
        self.muList = [0 for i in range(len(d.materialsList))]
        self.inventory = [0 for i in range(len(d.materialsList))]
        # TODO-DONE clear thoughts at the end of every week.
        self.thoughts = []
        # profiles
        self.knownPeople = {}
        self.knownManus = []
        self.knownStores = []
        self.knownHomes = []
        self.knownChurches = []
        self.knownUnitLists = [self.knownManus, self.knownStores, self.knownHomes, self.knownChurches]
        self.myProfile = self.peopleManager(self)
        self.myProfile.updateOpinion(100)
        self.myProfile.updateHouse(self.home, self.model.getDayNum())
        self.myProfile.updateBirthday(self.birthday)
        self.businesses = []
        # initial values
        self.allMu()
        self.maxSadness = sum(self.muList)
        self.isboss = False

    @property
    def name(self):
        return self.firstname + " " + self.lastname

    @name.setter
    def name(self, value):
        if len(value.split(' ')) >= 2:
            self.firstname, self.lastname = value.split(maxsplit=1)
        else:
            self.firstname = value
        self.peopleManager(self).name = value

    def workHandler(self):
        self.think("Off to work!")
        self.updateJobPrices()
        self.workConversations()

    def restHandler(self):
        self.think("I can finally relax a little.")
        self.jobHandler()
        self.friendConversations()
        self.eat()

    def shopHandler(self):
        self.allMu()
        self.goShopping()
        self.allMu()
        self.drink()

    def sleepHandler(self):
        self.think("My bed is so cozy.")
        self.update_my_profile()
        self.familyConversations()
        # TODO-DONE should eat 3x per day, 1 bread each time (or substitute good)
        # TODO eating, drinking should give MU
        self.eat()

    def jobHandler(self):
        if self.job is None:
            bestJob = self.jobSearch()

            if bestJob is not None:
                self.applyForJob(bestJob)
            else:
                self.think("I hate looking for jobs.")

    def churchHandler(self):
        if self.church is None:
            churchSearch = self.churchSearch()
            bestChurch = churchSearch[0]

            if bestChurch is not None:
                self.newChurch(bestChurch)
                self.think(f"I joined {bestChurch.name} today.")
                self.church.attend(self)
            else:
                self.think("I can't find a church in this neighborhood.")
        else:
            self.church.attend(self)

    def update_my_profile(self):
        profile = self.peopleManager(self)
        dayNum = self.model.clock.getDayNum()

        # profile.updateBirthday(self.birthday)
        profile.updateJob(self.job, dayNum)
        profile.updateHouse(self.home, dayNum)
        profile.updateMuList(self.muList, dayNum)

    # only bosses can create businesses
    def bossmaker(self):
        if not self.isboss:
            if self.capital >= 1000000 and self.model.char is not self:
                d.addBoss(self)
                self.isboss = True
                self.model.builder.newBusiness(self)

    def toString(self):
        name = self.getName()
        gender = self.genderCheck()
        homeAddress = str(self.getHome().getLocation())
        town = self.getLocality().getName()
        personsJob = self.getJob()

        if self.job != None:
            jobDescription = personsJob.getJobType()
        else:
            jobDescription = "Beggar"

        return f"{name} is a {gender} {jobDescription} who lives at {homeAddress} in {town}."

    def jobSearch(self):
        bestJob = None
        jobList = []

        for manu in self.knownManus:
            localJobList = manu.getStore().getJobs(self)
            jobList += localJobList

        for store in self.knownStores:
            localJobList = store.getStore().getJobs(self)
            jobList += localJobList

        for job in jobList:
            slots = job.getSlots()
            if slots > 0:
                if bestJob is None:
                    bestJob = job                
                else:
                    if job.getSalary() > bestJob.getSalary():
                        bestJob = job

        return bestJob

    def churchSearch(self):
        bestWeight = (None, 0)
        for church in self.knownChurches:
            if church.getReligion() == self.religion:
                pythTuple = self.pyth(church)
                distance = pythTuple[0]
                isLocal = pythTuple[1]

                weight = 1/distance

                if weight > bestWeight[1] or bestWeight[0] is None:
                    if isLocal:
                        bestWeight = (church, weight)

        return bestWeight
    
    def applyForJob(self, job):
        isHired = self.model.hirer.jobApplication(self, job)
        return isHired

    def updateJobPrices(self):
        #if works at market, update workplaces price profile
        workplace = None
        worksAtMarket = False

        if self.job is not None:
            workplace = self.job.getUnit()

        if workplace is not None:
            worksAtMarket = workplace.getMissions()[d.STORE_INDEX]
        
        if worksAtMarket:
            workProfile = self.unitManager(workplace)
            workPrices = workplace.getPrice()
            dayNum = workplace.getDayNum()
            workProfile.updatePrices(workPrices, dayNum)

            # thoughts
            self.think("I should check today's prices once I'm already here at work.")

    # sleep
    def spouseConversations(self):
        if self.spouse is not None:
            Convo.beginConversation(self, self.spouse)

    # work
    def workConversations(self):
        if self.job is not None:
            coworkers = self.job.getEmployees()
            totalCoworkers = len(coworkers)

            # numberOfConvos = random.randrange(4)
            numberOfConvos = 1
            if numberOfConvos > totalCoworkers:
                numberOfConvos = totalCoworkers

            # conversations
            for conversation in range(numberOfConvos):
                conversee = coworkers[random.randrange(totalCoworkers)]

                if conversee is not self:
                    Convo.beginConversation(self, conversee)

    # TODO fix this function so we can use it instead of spouseConversation
    def familyConversations(self):
        family = [x.person for x in self.peopleManager(self).getFamilyList()]
        # print([(x.firstname, x.lastname) for x in family])
        # family = [x.person for x in family]

        if len(family) > 0:
            conversee = random.choice(family)
            Convo.beginConversation(self, conversee)
        else:
            self.think("I'm all alone in the world.")

    def friendConversations(self):
        friend = self.randomPerson().person

        if friend is not self:
            Convo.beginConversation(self, friend)
            self.think(f"{friend.name} and I hung out this afternoon.")
        else:
            self.think("I enjoyed spending some time alone this afternoon.")

    def newChurch(self, church):
        self.church = church
        self.church.addMember(self)

    def getHappiness(self):
        sadness = sum(self.muList)
        happiness = 100 * ((self.maxSadness - sadness) / self.maxSadness)
        return happiness

    # TODO display player's MU curves as a graph, with a dot at current MU.
    # updates muList- run at start and end of shop state. We want it to be persistent even after they eat, for example
    # limit zeroes mu curve for each item
    # scale scales mu curve for each item
    def allMu(self):
        limitList = d.getUtilityLimit()
        scaleList = d.getUtilityScale()
        owned = self.home.getAllOutput()

        # muList calc
        muList = [0 for item in owned]

        for itemIndex in range(len(owned)):
            itemCount = owned[itemIndex]
            if itemCount == 0:
                itemCount = .1

            limit = limitList[itemIndex]
            scale = scaleList[itemIndex]
            mu = self.singleMu(itemIndex, itemCount)
            muList[itemIndex] = mu
        
        self.muList = muList

    def singleMu(self, i, count):
        limitList = d.getUtilityLimit()
        scaleList = d.getUtilityScale()
        
        limit = limitList[i]
        scale = scaleList[i]
       
        mu = scale * ((math.sqrt(limit) / math.sqrt(count)) - 1)

        return mu

    def muCurves(self):
        """Get marginal utility curves for plotting. Use self.allMu() for marginal utility."""
        limitList = d.getUtilityLimit()
        # scaleList = d.getUtilityScale()

        all_xs = []
        all_ys = []
        legend = []

        for i in range(len(limitList)):
            xs = []
            ys = []

            for c in range(limitList[i]+1):
                if c == 0:
                    c = .1
                mu = self.singleMu(i, c)
                xs.append(c)
                ys.append(mu)

            if len(xs) > 1:
                all_xs.append(xs)
                all_ys.append(ys)
                legend.append(d.getMaterials()[i])

        return all_xs, all_ys, legend

    def goShopping(self):
        p_chosenStore = self.chooseStore()[0]
        if p_chosenStore is not None:
            store = p_chosenStore.store
            self.purchase(store)
            self.storeAtHome()
        else:
            self.think("I don't know of any stores.")

    def pyth(self, unit):
        """Distance metric."""
        locality = unit.getLocality()
        location = unit.getLocation()
        isLocal = False

        # distance
        if (locality == self.locality) and (location is not None):
            distanceX = self.location[0] - location[0]
            distanceY = self.location[1] - location[1]
            distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
            isLocal = True
        else:
            # distance must be defined and != 0
            distance = 1000000
        return distance, isLocal

    def chooseStore(self):
        """returns (storeProfile, weight)"""
        # weights
        F = 1
        E = 2
        D = 1
        bestWeight = (None, 0)

        # possible stores

        for store in self.possStores():
            # vars
            familiarity = store.getFamiliarity()
            experience = store.getExperience()
            avgPrices = store.getPrices()

            # distance
            distance, isLocal = self.pyth(store)

            # desiredItemWeight
            muList = self.getMuList()
            maxMu = max(muList)
            price = avgPrices[muList.index(maxMu)]

            if price != 0:
                desiredItemWeight = maxMu/price
            else:
                desiredItemWeight = 0

            # formula
            weight = (1 / distance) * (familiarity * F) * (experience * E) * (desiredItemWeight * D)
            
            if (weight > bestWeight[1]) or (bestWeight[0] is None):
                if isLocal:
                    bestWeight = (store, weight)
        # thoughts
        if bestWeight[0] is not None:
            self.think(f"{bestWeight[0].name} seems like a good place to shop.")
        else:
            self.think("I can't think of anywhere to go shopping.")

        return bestWeight

    def possStores(self):
        possStores = []

        for store in self.knownStores:
            if store.familiarity == 1:
                self.think(f"I want to check out that new place I heard about, {store.name}.")
                possStores = [store]
                break
            else:
                possStores.append(store)

        return possStores

    def canAfford(self, amount):
        if self.capital >= amount:
            return True
        else:
            return False

    def purchase(self, store):
        buyMore = True
        price = store.getPrice()
        cash = self.capital
        muList = self.muList
        buy = [0 for i in d.getMaterials()]
        value = [self.muList[i] / price[i] if price[i] != 0 else 0 for i in range(len(self.muList))]
        # we don't want them to spend all their money on overpriced stuff- they'll need it tomorrow! Utility of money is CONSTANT.
        MONEYUTIL = 1

        while True:
            i = value.index(max(value))

            if (value[i] < MONEYUTIL) or (cash < price[i]):
                break

            bestPrice = price[i]
            cash -= bestPrice
            buy[i] += 1
            value[i] = (self.singleMu(i, self.home.output[i] + buy[i]) / price[i])

        if sum(buy) > 0:
            (amounts, cost, sold) = store.sell(self, copy.copy(buy))

            if sold:
                if amounts == buy:
                    self.think(f"I bought {self.listtostr(amounts)} for {str(cost)} ducats today at {store.name}.")
                else:
                    self.think(f"I went to buy {self.listtostr(buy)} at {store.name} but they only had {self.listtostr(amounts)}.")
            else:
                self.think(f"I went to {store.name} to buy {self.listtostr(buy)} but they ran out. Very annoying!")
        else:
            sold = False
            self.think(f"I don't really need anything from {store.name}. What a waste of time.")

        # update profile
        self.updateStore(store, sold)        

    def listtostr(self, array):
        string = ""
        for i in range(len(array)):
            if array[i] > 0:
                string += str(array[i]) + " " + d.getMaterials()[i] + ", "
        string = string[:-2]

        return string

    def updateStore(self, store, sold):
        storeProfile = self.unitManager(store)
        price = store.getPrice()
        # familiarity = storeProfile.getFamiliarity()
        experience = storeProfile.getExperience()        

        # familiarity increases with each visit
        storeProfile.updateFamiliarity()
        
        # experience should increase only if they had a good experience
        if sold:
            experience = experience * 1.1
        else:
            experience = experience / 1.1

        storeProfile.updateExperience(experience)

        # price
        storeProfile.updatePrices(price, store.getLocality().getDayNum())

    def storeAtHome(self):
        storage = self.home.output
        for i in range(len(self.inventory)):
            amount = self.inventory[i]
            self.inventory[i] -= amount
            storage[i] += amount

    def eat(self):
        storage = self.home.output
        if storage[d.BREAD_INDEX] >= 1:
            storage[d.BREAD_INDEX] -= 1
            self.think("I ate some delicious bread today.")
        else:
            self.think("I'm starving! I don't want to die!")

    # TODO add pubs
    def drink(self):
        storage = self.home.output
        if storage[d.BEER_INDEX] >= 1:
            storage[d.BEER_INDEX] -= 1
            self.think("That was a delicious beer!")
        else:
            self.think("I could really use a beer right now.")

    # TODO-DECIDE this function is weird and I don't know why. Just use random.choice?
    def randomManu(self, oldManu=None):
        length = len(self.knownManus)
        if length >= 2:
            manuIndex = random.randint(0, length-1)
            tryManu = self.knownManus[manuIndex]

            if (tryManu is not oldManu) or (oldManu is None):
                newManu = tryManu
            else:
                newManu = self.randomManu(oldManu)
        
        elif length == 1 and oldManu == None:
            newManu= self.knownManus[0]
        
        else:
            newManu = None
        
        return newManu

    def randomPerson(self, oldPerson=None):
        length = len(self.knownPeople)
        if length >= 2:
            tryPerson = self.knownPeople[random.choice(list(self.knownPeople.keys()))]

            if (tryPerson is not oldPerson) or (oldPerson is None):
                newPerson = tryPerson
            else:
                newPerson = self.randomPerson(oldPerson)

        elif length == 1 and oldPerson == None:
            newPerson = self.knownPeople[list(self.knownPeople.keys())[0]]

        else:
            newPerson = None

        return newPerson

    def randomStore(self, oldStore=None):
        length = len(self.knownStores)
        if length >= 2:
            storeIndex = random.randint(0, length-1)
            tryStore = self.knownStores[storeIndex]

            if (tryStore is not oldStore) or (oldStore is None):
                newStore = tryStore
            else:
                newStore = self.randomStore(oldStore)
        
        elif length == 1 and oldStore == None:
            newStore = self.knownStores[0]
        
        else:
            newStore = None
        
        return newStore

    def peopleManager(self, target):        
        if target in self.knownPeople:
            targetProfile = self.knownPeople[target]
        else:
            targetProfile = PersonProfile(target)
            self.knownPeople[target] = targetProfile

        return targetProfile

    def unitManager(self, target, heardabout=None):
        from profiles import StoreProfile

        notFound = True
        missions = target.getMissions()

        # search
        for i in range(len(missions)):
            if missions[i] and notFound:

                unitList = self.knownUnitLists[i]
                for testProfile in unitList:
                    if testProfile.store is target:
                        targetProfile = testProfile
                        notFound = False
                        break
        # create
        if notFound:
            targetProfile = StoreProfile(target, heardabout)
            
            for i in range(len(missions)):
                if missions[i]:
                    unitList = self.knownUnitLists[i]
                    unitList.append(targetProfile)

        return targetProfile

    def think(self, thought):
        dayNum = self.model.getDayNum()
        weekDay = self.model.week.state
        date = self.model.calendar.date()
        state = self.model.clock.state
        thought = (dayNum, weekDay, date, state, thought)
        self.thoughts.append(thought)

        if self.model.char == self:
            self.model.out(str(thought[0]).ljust(6) + thought[1].ljust(10) + str(thought[2]).ljust(19) + thought[3].ljust(10) + thought[4] + "\n")

    def printThoughts(self):
        print(self.name, "thought:")
        print("Day:  " + "Weekday:  " + "Date:             " + "Period:   " + "Thought:")
        for thought in self.thoughts:
            print(str(thought[0]).ljust(6) + thought[1].ljust(10) + str(thought[2]).ljust(19) + thought[3].ljust(10) + thought[4])

    def getName(self):
        return self.name
        
    def getGender(self):
        return self.gender

    def getLocality(self):
        return self.locality

    def getHome(self):
        return self.home

    def setHome(self, home):
        self.home = home

    def getJob(self):
        return self.job

    def getBusinesses(self):
        return self.businesses

    def getMuList(self):
        return self.muList

    def getKnownPeople(self):
        return list(self.knownPeople.values())

    def getKnownStores(self):
        return self.knownStores

    def getKnownManus(self):
        return self.knownManus

    def getKnownChurches(self):
        return self.knownChurches

    def getSalary(self):
        return self.salary

    def setJob(self, job, salary):
        self.job = job
        self.salary = salary
        dayNum = self.model.clock.getDayNum()
        self.myProfile.updateJob(job, dayNum)

    def unsetJob(self):
        job = self.getJob()
        self.job = None
        dayNum = self.model.clock.getDayNum()
        self.myProfile.updateJob(None, dayNum)

    def genderCheck(self):
        if self.getGender() == 0:
            return "man"
        else:
            return "woman"

    def setSpouse(self, spouse):
        self.spouse = spouse
        if self.getGender() == 1:
            self.lastname = spouse.lastname
        self.peopleManager(self).updateFamily(spouse=(self.peopleManager(spouse), self.model.getDayNum()))
        self.peopleManager(spouse).updateFamily(spouse=(self.peopleManager(self), self.model.getDayNum()))

    def getCapital(self):
        return self.capital

    def addCapital(self, capital):
        self.capital += capital

    def addInventory(self, i_item, amount):
        self.inventory[i_item] += amount

    def getInventory(self):
        return self.inventory

    def getReligion(self):
        return self.religion
