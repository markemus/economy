import database as d
import copy

class PersonProfile(object):
    birthday = None
    job = (None, 0)
    spouse = (None, 0)
    house = (None, 0)
    person = None
    salary = (0, 0)

    def __init__(self, person, father=(None, -2), mother=(None, -2), spouse=(None, -2), siblings=(None, -2), children=(None, -2)):
        dayNum = person.getLocality().model.getDayNum()
        # self.name = person.name
        self.firstname = person.firstname
        self.lastname = person.lastname
        self.locality = person.locality
        self.meton = person.locality.date()
        self.children = (dayNum)
        self.person = person
        self.muList = ([0 for i in d.getMaterials()], 0)
        # self.skills = ([0 for i in d.getSkills()], 0)
        self.father = father
        self.mother = mother
        self.spouse = spouse
        self.siblings = siblings
        self.children = children
        self.opinion = 0

    @property
    def name(self):
        return self.firstname + " " + self.lastname

    @name.setter
    def name(self, value):
        if len(value.split()) >= 2:
            self.firstname, self.lastname = value.split(maxsplit=1)
        else:
            self.firstname = value

    def getOpinion(self):
        return self.opinion

    def updateOpinion(self, change):
        if self.opinion <= 99:
            self.opinion = (self.opinion + change if self.opinion + change <= 100 else 100)

    def updateBirthday(self, birthday):
        self.birthday = birthday

    def updateJob(self, job, dayNum):
        self.job = (job, dayNum)

    def updateSalary(self, salary, dayNum):
        self.salary = (salary, dayNum)

    def getFamily(self):
        return (self.father, self.mother, self.spouse, self.siblings, self.children)

    #if you don't care how they're related
    def getFamilyList(self):
        siblings = [sibling for sibling in self.siblings[:-1]] if self.siblings[0] is not None else []
        children = [child for child in self.children[:-1]] if self.children[0] is not None else []
        family = [self.father[0], self.mother[0], self.spouse[0]] + siblings + children
        family = [mem for mem in family if mem is not None]
        return family

    # TODO-DECIDE does this require a Profile or a People object?
    # daynums in params
    # this method is a sin
    def updateFamily(self, father=(None, -2), mother=(None, -2), spouse=(None, -2), siblings=(None, -2), children=(None, -2)):
        family = {"father": father, "mother": mother, "spouse": spouse, "siblings": siblings, "children": children}
        for title, relative in family.items():
            # compare daynum
            if (relative[0]) and (relative[-1] > getattr(self, title)[-1]):
                setattr(self, title, relative)

    def updateHouse(self, p_house, dayNum):
        self.house = (p_house, dayNum)

    def updateMuList(self, muList, dayNum):
        self.muList = (copy.copy(muList), dayNum)

    def getBirthday(self):
        return self.birthday

    def getHouse(self):
        return self.house
    
    def getJob(self):
        return self.job

    def getSalary(self):
        return self.salary

    # def getSkills(self):
    #     return self.skills

    def getFather(self):
        return self.father

    def getMother(self):
        return self.mother

    def getSpouse(self):
        return self.spouse

    def getSiblings(self):
        return self.siblings

    def getChildren(self):
        return self.children

    def getMuList(self):
        return self.muList

    def getPerson(self):
        return self.person

    def get_values(self):
        spreadsheet = []
        spreadsheet.append(["name", "job", "locality", "birthday", "spouse", "house"])
        spreadsheet.append([str(self.name), str(self.job), str(self.locality), str(self.birthday), str(self.spouse), str(self.house)])
        
        return spreadsheet

    def attribute_list(self, array, name):
        att_array = []
        
        for item in array:
            att = getattr(item, name)
            att_array.append(att)

        return att_array

    def get_values_dict(self):
        values_dict = {}
        empty = "???"

        values_dict["name"] = str(self.name)
        values_dict["locality"] = str(self.locality.name)
        values_dict["birthday"] = (str(self.birthday) if self.birthday is not None else empty)
        values_dict["job"] = (str(self.job[0].jobType + " at " + self.job[0].unit.name) if self.job[0] is not None else empty)
        values_dict["father"] = (str(self.father[0].name) if self.father[0] is not None else empty)
        values_dict["mother"] = (str(self.mother[0].name) if self.mother[0] is not None else empty)
        # values_dict["siblings"] = str(self.siblings) 
        # values_dict["children"] = str(self.children)
        values_dict["spouse"] = (str(self.spouse[0].name) if self.spouse[0] is not None else empty)
        values_dict["house"] = (str(self.house[0].location) if self.house[0] is not None else empty)
        values_dict["mu"] = str([round(x, 2) for x in self.muList[0]])
        # values_dict["skills"] = (str(self.skills) if self.skills[1] != 0 else empty)
        values_dict["opinion"] = (str(self.opinion))
        values_dict["meton"] = (str(self.meton))

        return values_dict

class StoreProfile(object):
    name = None
    locality = None    #city
    location = None    #address
    #fam and exp should never be negative. Fam increases by 1 EVERY VISIT and is updated BEFORE avgPrices
    familiarity = 1
    experience = 1
    store = None

    def __init__(self, store, heardabout=None):
        dayNum = store.getLocality().getDayNum()
        self.store = store
        self.location = store.getLocation()
        self.locality = store.getLocality()
        self.name = store.name
        self.avgPrices = ([0 for i in d.getMaterials()], dayNum)
        self.heardabout = str(heardabout.name if heardabout is not None else "Discovered") + " on " + str(store.getLocality().date())

    def get_values_dict(self):
        values_dict = {}
        values_dict["name"] = str(self.name)
        values_dict["prices"] = str(self.avgPrices)
        values_dict["familiarity"] = str(self.familiarity)
        values_dict["experience"] = str(self.experience)
        values_dict["locality"] = str(self.locality)
        values_dict["location"] = str(self.location)
        values_dict["heardabout"] = str(self.heardabout)

        return values_dict

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