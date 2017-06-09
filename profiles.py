import database as d

class PersonProfile(object):
    name = None
    locality = None
    birthday = None
    job = (None, 0)
    spouse = (None, 0)
    house = (None, 0)
    person = None

    def __init__(self, person):
        dayNum = person.getLocality().model.getDayNum()
        self.name = person.name
        self.children = ([], dayNum)
        self.person = person
        self.muList = [(0,0) for i in d.getMaterials()]

    def updateBirthday(self, birthday):
        self.birthday = birthday

    def updateJob(self, job, dayNum):
        self.job = (job, dayNum)

    #updateSpouse,Children,House take PROFILES as parameters
    def updateSpouse(self, p_spouse, dayNum):
        self.spouse = (p_spouse, dayNum)

    def updateChildren(self, p_child, dayNum):
        self.children[0].append(p_child)
        self.children = (self.children[0], dayNum)

    def updateHouse(self, p_house, dayNum):
        self.house = (p_house, dayNum)

    def updateMuList(self, muList, dayNum):
        self.muList = (muList, dayNum)

    def getBirthday(self):
        return self.birthday

    def getHouse(self):
        return self.house
    
    def getJob(self):
        return self.job

    def getSpouse(self):
        return self.spouse

    def getChildren(self):
        return self.children

    def getMuList(self):
        return self.muList

    def getPerson(self):
        return self.person

    def get_values(self):
        values_dict = {}
        values_dict["name"] = str(self.name)
        values_dict["locality"] = str(self.locality)
        values_dict["birthday"] = str(self.birthday)
        values_dict["job"] = str(self.job)
        values_dict["spouse"] = str(self.spouse)
        values_dict["house"] = str(self.house)

        return values_dict

class StoreProfile(object):
    name = None
    locality = None    #city
    location = None    #address
    #fam and exp should never be negative. Fam increases by 1 EVERY VISIT and is updated BEFORE avgPrices
    familiarity = 1
    experience = 1
    store = None

    def __init__(self, store):
        dayNum = store.getLocality().getDayNum()
        self.store = store
        self.location = store.getLocation()
        self.locality = store.getLocality()
        self.name = store.name
        self.avgPrices = ([0 for i in d.getMaterials()], dayNum)

    def updatePrices(self, prices, dayNum):
        n = self.familiarity
        newAvgPrices = self.avgPrices[0]

        #if first visit, avg prices are today's prices
        if n == 1:
            newAvgPrices = prices
        else:
            #We don't store the individual values, so we have to "unpack" the old avg and repack it. (ie find common denominator)
            for i in range(len(prices)):
                newAvgPrices[i] = ((newAvgPrices[i] * (n-1)/n)) + prices[i]/n

        self.avgPrices = (newAvgPrices, dayNum)

    def updateLocation(self, location):
        self.location = location

    def updateLocality(self, locality):
        self.locality = locality

    def updateFamiliarity(self):
        self.familiarity = self.familiarity + 1

    def updateExperience(self, experience):
        self.experience = experience

    def getPricesWithDayNum(self):
        return self.avgPrices

    def getPrices(self):
        return self.avgPrices[0]

    def getLocation(self):
        return self.location

    def getLocality(self):
        return self.locality

    def getFamiliarity(self):
        return self.familiarity

    def getExperience(self):
        return self.experience

    def getStore(self):
        return self.store