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
        self.local_map = [[None for x in range(width)] for y in range(height)]
        d.addLocality(self)

    def getName(self):
        return self.name

    def getWidth(self):
        return self.width

    def getMap(self):
        return self.local_map

    def claim_node(self, xy, entity):
        claimed = False
        x = xy[0]
        y = xy[1]

        if self.local_map[x][y] is None:
            self.local_map[x][y] = entity
            claimed = True

        return claimed
    
    def check_node(self, node):
        is_empty = False
        
        if node is None:
            is_empty = True
        
        return is_empty

    #algorithm checks indices reflected around the diagonal, starting from upper left
    #I feel like this algorithm is confusing, but it's the best I can do right now
    def find_property(self):
        xy = None

        for i in range(len(self.local_map)):

            j = 0
            
            if xy is not None:
                break

            while i >= j:
                if self.check_node(self.local_map[i][j]):
                    xy = (i,j)
                    break
                if self.check_node(self.local_map[j][i]):
                    xy = (j,i)
                    break
                j += 1

        return xy

    def printMap(self):

        print(self.name)

        mLocalMap = self.getMap()

        for row in mLocalMap:
            
            rowAppearance = ""
            
            for i in row:

                if (i == None):
                    rowAppearance = rowAppearance + "."

                else:
                    rowAppearance = rowAppearance + i.character
            
            print(rowAppearance)

    def getDayNum(self):
        return self.model.getDayNum()