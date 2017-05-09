import database as d
import math
import random
from conversation import Convo

class People:
    name = "John Doe"
    gender = 0                          #0 are men, 1 are women
    age = 0
    locality = None                     #a localMap
    home = None                         #a Unit in homeTown
    skills = [0,0,0,0,0,0,0,0,0,0]      #each index represents a particular skill- shoemaking, or lumberjacking, etc.
    job = None                          #None is unemployed
    salary = 0
    capital = 0
    spouse = None
    church = None

    def __init__(self, model, theirName, theirGender, theirAge, theirHometown, theirHome, theirSkills, theirReligion):
        d.addPeople(self)
        self.model = model
        self.name = theirName
        self.gender = theirGender
        self.age = theirAge
        self.locality = theirHometown
        self.home = theirHome
        self.location = theirHome.location
        self.skills = theirSkills
        self.religion = theirReligion
        self.muList = [0 for i in range(len(d.materialsList))]
        self.inventory = [0 for i in range(len(d.materialsList))]
        self.thoughts = []
        #profiles
        self.knownPeople = []
        self.knownManus = []
        self.knownStores = []
        self.knownHomes = []
        self.knownChurches = []
        self.knownUnitLists = [self.knownManus, self.knownStores, self.knownHomes, self.knownChurches]
        self.myProfile = self.peopleManager(self)
        self.businesses = []
        #initial values
        self.marginalUtility()

    def sleepHandler(self):
        self.think("My bed is so cozy.")
        self.eat()
        self.drink()

    def workHandler(self):
        self.think("Off to work!")
        self.updateJobPrices()
        self.workConversations()

    def restHandler(self):
        self.think("I can finally relax a little.")
        self.jobHandler()

    def shopHandler(self):
        self.marginalUtility()
        self.goShopping()
        self.marginalUtility()

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
                self.think("I joined ", bestChurch.name, " today.")
            else:
                self.think("I can't find a church in this neighborhood.")
        else:
            self.church.attend(self)

    def toString(self):
        name = self.getName()
        gender = self.genderCheck()
        homeAddress = str(self.getHome().getLocation())
        town = self.getLocality().getName()
        personsJob = self.getJob()

        if (gender == "man"):
            genderPronoun = "He"
        else:
            genderPronoun = "She"

        if (self.job != None):
            jobDescription = personsJob.getJobType()
        else:
            jobDescription = "Beggar"

        return(name + " is a " + gender + " who lives at " + homeAddress + " in " 
            + town + ". " + genderPronoun + " works as a " + jobDescription + ".")

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

            #thoughts
            self.think("I should check today's prices once I'm already here at work.")

    def workConversations(self):
        #talk to some people at work
        if self.job is not None:
            coworkers = self.job.getEmployees()
            totalCoworkers = len(coworkers)

            numberOfConvos = random.randrange(4)
            if numberOfConvos > totalCoworkers:
                numberOfConvos = totalCoworkers

            #conversations
            for conversation in range(numberOfConvos):
                conversee = coworkers[random.randrange(totalCoworkers)]

                if conversee is not self:
                    Convo.beginConversation(self, conversee)

    def newChurch(self, church):
        self.church = church
        self.church.addMember(self)

    def getHappiness(self):
        totalSadness = 0
        for i in self.muList:
            totalSadness += i
        happiness = round(d.getMaxHappiness() - totalSadness)
        return happiness

    #updates muList- run at start of shop state.
    #limit zeroes mu curve for each item
    #scale scales mu curve for each item
    def marginalUtility(self):
        limitList = d.getUtilityLimit()
        scaleList = d.getUtilityScale()

        #owned
        if self.home != None:
            owned = self.home.getAllOutput()
        else:
            owned = [0 for item in limitList]

        #muList calc
        muList = [0 for item in owned]

        for itemIndex in range(len(owned)):
            itemCount = owned[itemIndex]
            if itemCount == 0:
                itemCount = .1

            limit = limitList[itemIndex]
            scale = scaleList[itemIndex]
            mu =  scale * ((math.sqrt(limit) / math.sqrt(itemCount)) - 1)
            muList[itemIndex] = mu
        
        self.muList = muList

    def goShopping(self):
        p_chosenStore = self.chooseStore()[0]
        if p_chosenStore is not None:
            store = p_chosenStore.store
            self.purchase(store)
            self.storeAtHome()
        else:
            self.think("I don't know of any stores.")

    def pyth(self, unit):
        locality = unit.getLocality()
        location = unit.getLocation()
        #distance
        if (locality == self.locality) and (location is not None):
            distanceX = self.location[0] - location[0]
            distanceY = self.location[1] - location[1]
            distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
            isLocal = 1
        else:
            #distance must be defined and != 0
            distance = 1000000
        return (distance, isLocal)

    def chooseStore(self):
        F = 1
        E = 1
        D = 1
        bestWeight = (None, 0)

        for store in self.knownStores:
            locality = store.getLocality()
            location = store.getLocation()
            familiarity = store.getFamiliarity()
            experience = store.getExperience()
            avgPrices = store.getPrices()
            isLocal = 0

            #distance
            pythTuple = self.pyth(store)
            distance = pythTuple[0]
            isLocal = pythTuple[1]

            #desiredItemWeight
            muList = self.getMuList()
            mu = max(muList)
            i = muList.index(mu)
            price = avgPrices[i]

            if price != 0:
                desiredItemWeight = mu/price
            else:
                desiredItemWeight = 0

            #formula
            weight = (1 / distance) * (familiarity * F) * (experience * E) * (desiredItemWeight * D)
            
            if (weight > bestWeight[1]) or (bestWeight[0] is None):
                if (isLocal == 1):
                    bestWeight = (store, weight)
        #thoughts                    
        if bestWeight[0] is not None:
            self.think(bestWeight[0].name + " seems like a good place to shop.")
        else:
            self.think("I can't think of anywhere to go shopping.")
        return bestWeight

    def purchase(self, store):
        price = store.getPrice()
        value = [0 for item in self.muList]
        i_bestValue = 0
        bestPrice = 0
        isAbleToAffordAnything = False
        sold = False

        #find optimal
        for i in range(len(self.muList)):
            if price[i] == 0:
                thisValue = 0
            else:
                thisValue = self.muList[i] / price[i]
            thisPrice = price[i]
            value[i] = thisValue
            #not optimal- if w,x,y,z with mu/price in that order, what if I can afford either w+z or x+y? NP problem.
            if thisValue > value[i_bestValue] and thisPrice < self.capital:
                i_bestValue = i
                bestPrice = thisPrice
                isAbleToAffordAnything = True

        #purchase
        if isAbleToAffordAnything:
            sold = store.sell(self, 1, i_bestValue)

        #update profile
        storeProfile = self.unitManager(store)
        familiarity = storeProfile.getFamiliarity()
        experience = storeProfile.getExperience()        

        #familiarity should increase with each visit
        storeProfile.updateFamiliarity()
        
        #experience should increase only if they had a good experience- rudimentary
        if sold:
            experience = experience * 1.1
        else:
            experience = experience / 1.1

        storeProfile.updateExperience(experience)

        #price
        storeProfile.updatePrices(price, store.getLocality().getDayNum())

        #thoughts
        if sold:
            item = d.getMaterials()[i_bestValue]
            self.think("I bought a " + item + " today at " + store.name + " for " + str(bestPrice) + " ducats.")
        else:
            self.think("I can't afford anything at " + store.name)

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

    def drink(self):
        storage = self.home.output
        if storage[d.BEER_INDEX] >= 1:
            storage[d.BEER_INDEX] -= 1
            self.think("That was a delicious beer!")
        else:
            self.think("I could really use a beer right now.")

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
            personIndex = random.randint(0, length-1)
            tryPerson = self.knownPeople[personIndex]

            if (tryPerson is not oldPerson) or (oldPerson is None):
                newPerson = tryPerson
            else:
                newPerson = self.randomPerson(oldPerson)
        
        elif length == 1 and oldPerson == None:
            newPerson = self.knownPeople[0]
        
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
        from profiles import PersonProfile

        notFound = True
        for testProfile in self.knownPeople:
            if testProfile.person is target:
                targetProfile = testProfile
                notFound = False
                break
        
        if notFound:
            targetProfile = PersonProfile(target)
            self.knownPeople.append(targetProfile)

        return targetProfile

    def unitManager(self, target):

        from profiles import StoreProfile

        notFound = True
        missions = target.getMissions()

        #search
        for i in range((len(missions))):
            if missions[i] and notFound:

                unitList = self.knownUnitLists[i]
                for testProfile in unitList:
                    if testProfile.store is target:
                        targetProfile = testProfile
                        notFound = False
                        break
        #create
        if notFound:
            targetProfile = StoreProfile(target)
            
            for i in range(len(missions)):
                if missions[i]:
                    unitList = self.knownUnitLists[i]
                    unitList.append(targetProfile)

        #return
        return targetProfile

    def think(self, thought):
        dayNum = self.model.getDayNum()
        weekDay = self.model.week.state
        date = self.model.calendar.date()
        state = self.model.clock.state
        thought = (dayNum, weekDay, date, state, thought)
        self.thoughts.append(thought)

    def printThoughts(self):
        print(self.name, "thought:")
        print("Day:  " + "Weekday:  " + "Date:             " + "Period:   " + "Thought:")
        for thought in self.thoughts:
            print(str(thought[0]).ljust(6) + thought[1].ljust(10) + str(thought[2]).ljust(18) + thought[3].ljust(10) + thought[4])

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

    def getAge(self):
        return self.age

    def getLocality(self):
        return self.locality

    def getHome(self):
        return self.home

    def getJob(self):
        return self.job

    def getBusinesses(self):
        return self.businesses

    def getMuList(self):
        return self.muList

    def getKnownPeople(self):
        return self.knownPeople

    def getKnownStores(self):
        return self.knownStores

    def getKnownManus(self):
        return self.knownManus

    def getSalary(self):
        return self.salary

    def getSkill(self, skillIndex):
        return self.skills[skillIndex]

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
            return("man")
        else:
            return("woman")

    def getCapital(self):
        return self.capital

    def addCapital(self, capital):
        self.capital += capital

    def addInventory(self, i_item, amount):
        self.inventory[i_item] += amount

    def getInventory(self):
        return self.inventory