from random import shuffle

import clock

# TODO update meat and fruit. Replacement goods for bread.
# indices
GRAIN_INDEX = 0
FLOUR_INDEX = 1
BEER_INDEX  = 2
BREAD_INDEX = 3
MEAT_INDEX  = 4
FRUIT_INDEX = 5
LUMBER_INDEX  = 6
CHAIR_INDEX = 7
TABLE_INDEX = 8 

# TODO-DECIDE reconcile with zoning?
# profile indices
MANU_INDEX = 0
STORE_INDEX = 1
HOME_INDEX = 2
CHURCH_INDEX = 3

# required stock- empty list if none
# each tuple contains indexes of required inputs and the ratio of input to output. eg 1 flour needs only 2 grain.
# harvest inputs are currently placeholders
grain   = []
# grain   = [(GRAIN_INDEX, .04)]
flour   = [(GRAIN_INDEX, 1)]
beer    = [(GRAIN_INDEX, 1/1000)]
bread   = [(FLOUR_INDEX, .02)]
meat    = []
fruit   = []
lumber    = []
chair   = [(LUMBER_INDEX, 35)]
table   = [(LUMBER_INDEX, 100)]

components = [grain, flour, beer, bread, meat, fruit, lumber, chair, table]

# growth ratios
# plant 1 grain, harvest X grain
growratios = []

# Units of measurement- for reference.
material_units = {"grain": "bushels", "flour": "kg", "beer": "pint", "bread": "loaf", "meat": None, "fruit": None, "lumber": None, "chair": None, "table": None}

# production types
planted = ["grain", "beer", "meat", "fruit", "lumber"]
crafted = ["flour", "bread", "chair", "table"]

# planting seasons- only grain for now (which is winter wheat)
seasons = [["September", "October", "April", "May"], "all", "all", "all", "all", "all", "all", "all", "all"]

# name lists
maleNameList = open("boynames", "r").read().splitlines()
femaleNameList = open("girlnames", "r").read().splitlines()
lastNameList = open("lastnames", "r").read().splitlines()
busiNameList = open("businessnames", "r").read().splitlines()

# these are identified by these same indices throughout the program.
equipmentList = ["millstone"]
skillsList = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# TODO more products.
materialsList = ["grain", "flour", "beer", "bread", "meat", "fruit", "lumber", "chair", "table"]
unitMissions = ["manu", "store", "house", "church"]

# game objects
# TODO-DONE HOW MANY OF THESE ARE ACTUALLY USED?
localityList = []
businessList = []
religionList = []
unitList = []
churchList = []
peopleList = []
bossList = []
houseList = []

# utility
# people will buy up to the number below EXCLUSIVE.
utilityLimitList = [0, 0, 7, 14, 0, 0, 0, 3, 2]
utilityScaleList = [0, 0, 50, 50, 0, 0, 0, 300, 300]
# happinessMax = sum( utilityLimitList[i] * utilityScaleList[i] for i in range(len(utilityLimitList)))

def addBusiness(business):
    businessList.append(business)

def addLocality(locality):
    localityList.append(locality)

def addPeople(person):
    peopleList.append(person)

def addHouse(house):
    houseList.append(house)

def addBoss(boss):
    bossList.append(boss)

def removeBoss(boss):
    bossList.remove(boss)

def addUnit(unit):
    unitList.append(unit)

def addReligion(religion):
    religionList.append(religion)

def addChurch(church):
    addUnit(church)
    churchList.append(church)

def getReligions():
    return religionList

def getBosses():
    return bossList

def getChurches():
    return churchList

def getBusinesses():
    return businessList

def getEquipment():
    return equipmentList

def getFirstNameList(gender):
    if gender == 0:
        nameList = maleNameList
    else:
        nameList = femaleNameList
    return nameList

def getLastNameList():
    return lastNameList

def getLocality():
    return localityList

def getMaxHappiness():
    return happinessMax

def getMaterials():
    return materialsList

def getComponents(materialIndex):
    return components[materialIndex]

def getAllComponents():
    return components

def getSkills():
    return skillsList

def getPeople():
    return peopleList

def getHouses():
    return houseList

def shufflePeople():
    shuffle(peopleList)

def getUnit():
    return unitList

def getUnitMissions():
    return unitMissions

def getUtilityLimit():
    return utilityLimitList

def getUtilityScale():
    return utilityScaleList

def is_planted(materialIndex):
    is_planted = False
    material = materialsList[materialIndex]
    
    if material in planted:
        is_planted = True

    return is_planted

def is_crafted(materialIndex):
    is_crafted = False
    material = materialsList[materialIndex]

    if material in crafted:
        is_crafted = True

    return is_crafted

def getSeasons():
    return seasons

def isInSeason(materialIndex, month):
    if (seasons[materialIndex] == "all") or (month in seasons[materialIndex]):
        return True
    else:
        return False

# def getPlantingDays(materialIndex):
#     if seasons[materialIndex] == "all":
#         planting_days = 365
#     else:
#         planting_days = 0
#         for month in seasons[materialIndex]:
#             # Special case
#             if month == "January":
#                 planting_days += clock.SecularCalendar.daysPerMonth[0]
#             else:
#                 month_idx = clock.SecularCalendar.months.index(month)
#                 planting_days += clock.SecularCalendar.daysPerMonth[month_idx]
#
#     return planting_days
