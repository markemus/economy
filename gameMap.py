import numpy as np

import database as d
import clock

# world map made up of ALL localities (for particular installation, or otherwise compartmentalize)
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


# town map made up of nodes
class Locality(object):
    def __init__(self, model, location, width, height, name):
        self.model = model
        self.width = width
        self.height = height
        self.name = name
        self.location = location
        # Should be dtype object so we can store buildings. We'll use that for both.
        self.local_map = np.array([[None for x in range(width)] for y in range(height)])
        self.zoning_map = np.array([["_" for x in range(width)] for y in range(height)])
        self.make_zoning()
        d.addLocality(self)

    def getName(self):
        return self.name

    def getWidth(self):
        return self.width

    def getBuildingMap(self):
        return self.local_map

    def getZoningMap(self):
        """Determines which buildings can be built at each location on the map.
        Lower case means unoccupied."""
        return self.zoning_map

    def make_zoning(self):
        """Build the zoning_map. Optimized for locality(100,100)."""
        zmap = self.getZoningMap()
        center = (zmap.shape[0] // 2, zmap.shape[1] // 2)
        # Fields- surrounding city
        zmap[:, :] = "f"
        # city boundaries
        outskirts = [[center[0]-center[0]//2, center[0]+center[0]//2], [center[1]-center[1]//2, center[1]+center[1]//2]]
        # Housing- surrounding city center.
        zmap[outskirts[0][0]: outskirts[0][1], outskirts[1][0]: outskirts[1][1]] = "h"
        # Businesses on roads through housing
        for r in range(outskirts[0][0], outskirts[0][1], 25)[1:]:
            zmap[outskirts[1][0]:outskirts[1][1], r] = "b"
        for r in range(outskirts[1][0], outskirts[1][1], 25)[1:]:
            zmap[r, outskirts[0][0]:outskirts[0][1]] = "b"
        # City center- businesses
        zmap[center[0]-3: center[0]+3, center[1]-3: center[1]+3] = "b"
        # City hall- central spot
        zmap[center[0], center[1]] = "c"

    def claim_node(self, xy, entity):
        claimed = False
        x = xy[0]
        y = xy[1]

        if self.local_map[x][y] is None:
            self.local_map[x][y] = entity
            self.zoning_map[x, y] = self.zoning_map[x, y].upper()
            claimed = True

        return claimed
    
    def check_node(self, node):
        is_empty = False
        
        if node is None:
            is_empty = True
        
        return is_empty

    def find_property(self, zone):
        """Selects a random plot for use."""
        zone_map = self.getZoningMap()
        available_plots = np.argwhere(zone_map==zone)
        np.random.shuffle(available_plots)
        if len(available_plots):
            location = available_plots[0]
        else:
            location = None

        return location

    def printMap(self):
        print(self.name)
        mLocalMap = self.getBuildingMap()

        for row in mLocalMap:
            rowAppearance = ""
            
            for i in row:
                if (i == None):
                    rowAppearance = rowAppearance + "."
                else:
                    rowAppearance = rowAppearance + i.character
            
            print(rowAppearance)

    # TODO-DECIDE player's properties should be bolded?
    def get_print_map(self):
        print_map = ""

        for row in self.local_map:
            rowAppearance = ""
            
            for i in row:
                if (i == None):
                    rowAppearance = rowAppearance + "_"
                else:
                    rowAppearance = rowAppearance + i.character
            
            print_map += rowAppearance + "\n"

        return print_map

    def get_zoning_print_map(self):
        """Generates a printable map of the locality's zoning."""
        print_map = ""

        for row in self.zoning_map:
            rowAppearance = ""

            for x in row:
                rowAppearance = rowAppearance + x

            print_map += rowAppearance + "\n"

        return print_map

    def getDayNum(self):
        return self.model.getDayNum()

    def date(self):
        return self.model.calendar.date()
