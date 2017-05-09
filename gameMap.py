import database as d
import clock

#world map made up of ALL localities (for particular installation, or otherwise compartmentalize)
class World(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getMap(self):

        mWorldMap = [[None for y in range(self.height)] for x in range(self.width)]

        #all localities share char T for now
        for locality in d.getLocality():
            x = locality.location[0]
            y = locality.location[1]
            mWorldMap[x][y] = "T"

        return mWorldMap

    def printMap(self):

        print("The Known World")

        mWorldMap = self.getMap()
        mapHeight = len(mWorldMap[0])
        y = 0

        while (y < mapHeight):

            rowAppearance = ""

            for col in mWorldMap:

                if (col[y] == None):
                    rowAppearance = rowAppearance + "."
                else:
                    rowAppearance = rowAppearance + col[y]

            print(rowAppearance)

            y += 1






#town map made up of nodes
class Locality(object):

    def __init__(self, model, location, width, height, name):
        self.model = model
        self.width = width
        self.height = height
        self.name = name
        self.location = location
        # self.clock = clock.Clock(self)
        # self.week = clock.Week()
        # self.calendar = clock.SecularCalendar()
        d.addLocality(self)

    def getName(self):
        return self.name

    def getWidth(self):
        return self.width

    # temporarily getMap draws from unitList until database is established (should use api anyway)
    def getMap(self):
        
        mLocalMap = [[None for y in range(self.height)] for x in range(self.width)]

        for node in d.getUnit():
            if (node.getLocality() == self):
                x = node.location[0]
                y = node.location[1]
                mLocalMap[x][y] = node.character

        return mLocalMap

    def printMap(self):

        print(self.name)

        mLocalMap = self.getMap()
        mapHeight = len(mLocalMap[0])
        y = 0

        while (y < mapHeight):
            
            rowAppearance = ""
            
            for col in mLocalMap:

                if (col[y] == None):
                    rowAppearance = rowAppearance + "."

                else:
                    rowAppearance = rowAppearance + col[y]
            
            print(rowAppearance)
            y += 1

    def getDayNum(self):
        return self.model.getDayNum()