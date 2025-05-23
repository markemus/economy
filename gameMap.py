import math
import random

import numpy as np

import ai
import business as bus
import database as d
import people as p
import unit as u


# world map made up of ALL localities (for particular installation, or otherwise compartmentalize)
class World:
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
class Locality:
    def __init__(self, model, location, width, height, name):
        self.model = model
        self.width = width
        self.height = height
        self.name = name
        self.location = location
        # Government will be created after people are generated
        self.government = None
        self.town_hall = None
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

    # TODO-DONE forest zone(s)
    # TODO-DONE river with neighboring mill zones
    def make_zoning(self):
        """Build the zoning_map. Optimized for locality(100,100)."""
        zmap = self.getZoningMap()
        bmap = self.getBuildingMap()
        center = (zmap.shape[0] // 2, zmap.shape[1] // 2)
        # Fields- surrounding city
        zmap[:, :] = "f"
        # Forest - in the fields
        poss_f_centroids = np.argwhere(zmap == "f")
        np.random.shuffle(poss_f_centroids)
        f_centroids = poss_f_centroids[:random.randint(5, 15)]
        for f_centroid in f_centroids:
            xspread = random.randint(3, 5)
            yspread = random.randint(3, 5)
            zmap[f_centroid[0]-xspread: f_centroid[0]+xspread, f_centroid[1]-yspread: f_centroid[1]+yspread] = "w"
            zmap[f_centroid[0]-xspread-random.randint(0, 3): f_centroid[0]+xspread+random.randint(0, 3), f_centroid[1]-yspread: f_centroid[1]+yspread] = "w"
            zmap[f_centroid[0]-xspread: f_centroid[0]+xspread, f_centroid[1]-yspread-random.randint(0, 3): f_centroid[1]+yspread+random.randint(0, 3)] = "w"
            zmap[f_centroid[0]-xspread-random.randint(2, 5): f_centroid[0]+xspread+random.randint(2, 5), f_centroid[1]-yspread: f_centroid[1]+yspread] = "w"
            zmap[f_centroid[0]-xspread: f_centroid[0]+xspread, f_centroid[1]-yspread-random.randint(2, 5): f_centroid[1]+yspread+random.randint(2, 5)] = "w"

        # city boundaries
        outskirts = [[center[0]-center[0]//2, center[0]+center[0]//2], [center[1]-center[1]//2, center[1]+center[1]//2]]
        # Housing- surrounding city center.
        zmap[outskirts[0][0]: outskirts[0][1], outskirts[1][0]: outskirts[1][1]] = "h"

        # Business zoning on roads through city.
        for road in range(random.randint(4, 10)):
            b_direction = (0, 0)
            b_location = (random.randint(outskirts[0][0], outskirts[0][1]), random.randint(outskirts[1][0], outskirts[1][1]))
            while (outskirts[0][0] < b_location[0] < outskirts[0][1]) and (outskirts[1][0] < b_location[1] < outskirts[1][1]):
                # print(b_location)
                zmap[b_location] = "b"
                # bmap[b_location] = "b"
                if not random.randint(0, 5):
                    b_direction = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
                b_location = (b_location[0] + b_direction[0], b_location[1] + b_direction[1])

        # City center- businesses
        zmap[center[0]-2: center[0]+3, center[1]-2: center[1]+3] = "b"
        # bmap[center[0]-2: center[0]+3, center[1]-2: center[1]+3] = "b"
        # City hall- central spot
        zmap[center[0], center[1]] = "t"

        # TODO-DONE once we add town hall ("c"), make the river go around it if it needs to.
        # River
        r_direction = (1, 1)
        r_location = (0, random.randint(0, zmap.shape[1] // 2))
        while (r_location[0] < zmap.shape[0]) and (r_location[1] < zmap.shape[1]):
            zmap[r_location] = "r"
            bmap[r_location] = "r"
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if (0 <= r_location[0] + x < zmap.shape[0]) and (0 <= r_location[1] + y < zmap.shape[1]):
                        if zmap[r_location[0]+x, r_location[1]+y] not in ["r", "t"]:
                            zmap[r_location[0] + x, r_location[1] + y] = "m"
                            bmap[r_location[0] + x, r_location[1] + y] = None
            if not random.randint(0, 5):
                r_direction = random.choice([(1, 0), (1, 1), (0, 1), (1, 1)])

            prop_location = (r_location[0] + r_direction[0], r_location[1] + r_direction[1])
            # If prop_location is reserved for city hall, we'll just try again next round.
            if not (prop_location[0] < outskirts[0][1] and prop_location[1] < outskirts[1][1]) or not zmap[prop_location] == "t":
                r_location = prop_location

    def make_town_hall(self):
        """Builds town hall in the center of the locality."""
        # mayor = random.choice([p for p in d.getPeople() if not p.businesses and not isinstance(p, ai.Character)])
        home_location = self.find_property(zone="h")
        mayor_home = u.House(self, home_location)
        mayor = p.People(model=self.model, firstname="John", lastname="Meyer", theirGender=0, theirHometown=self, theirHome=mayor_home, theirReligion=random.choice(d.getReligions()))
        mayor.addCapital(200)
        mayor_home.addTenant(mayor)
        location = self.find_property(zone="t")
        self.government = bus.Business(owners=[mayor], name=f"City of {self.name}", busiLocality=self, busiCash=0)
        self.town_hall = u.TownHall(unitName=f"{self.name} City Hall", unitLocality=self, unitLocationTuple=location, business=self.government)
        self.claim_node(xy=location, entity=self.town_hall)
        self.claim_node(xy=home_location, entity=mayor_home)

    # TODO balance node pricing.
    def node_price(self, x, y):
        """Cost of a plot in the city."""
        pricing = {"t": 0,
                   "f": 100,
                   "w": 100,
                   "h": 100,
                   "b": 100,
                   "m": 100,
                   }

        return pricing[self.zoning_map[x, y]]

    def claim_node(self, xy, entity):
        claimed = False
        x = xy[0]
        y = xy[1]

        if self.local_map[x][y] is None:
            cost = self.node_price(x, y)

            if self.zoning_map[x, y] == "h":
                purchaser = entity.tenants[0]
            else:
                purchaser = entity.business

            if purchaser.canAfford(cost):
                purchaser.addCapital(-cost)
                self.government.addCapital(cost)
                self.local_map[x][y] = entity
                self.zoning_map[x, y] = self.zoning_map[x, y].upper()
                claimed = True

        return claimed

    def claim_nodes_from_topleft(self, xy, xsize, ysize, entity):
        """Claim a patch of map nodes."""
        claimed = False
        x = xy[0]
        y = xy[1]

        if (self.local_map[x:x+xsize, y:y+ysize] == None).all():
            cost = sum([sum([self.node_price(x, y) for y in range(y, y+ysize)]) for x in range(x, x+xsize)])

            if self.zoning_map[x, y] == "h":
                purchaser = entity.tenants[0]
            else:
                purchaser = entity.business

            if purchaser.canAfford(cost):
                purchaser.addCapital(-cost)
                self.government.addCapital(cost)
                self.local_map[x:x+xsize, y:y+ysize] = entity
                self.zoning_map[x:x+xsize, y:y+ysize] = self.zoning_map[x, y].upper()
                claimed = True

        return claimed

    def check_node(self, node):
        is_empty = False
        
        if node is None:
            is_empty = True
        
        return is_empty

    def pyth(self, xy1, xy2):
        distanceX = xy1[0] - xy2[0]
        distanceY = xy1[1] - xy2[1]
        distance = math.sqrt(distanceX ** 2 + distanceY ** 2)

        return distance

    def find_property(self, zone, owner=None):
        """Selects a nearby plot for use."""
        zone_map = self.getZoningMap()
        available_plots = np.argwhere(zone_map==zone)
        if owner:
            available_plots = sorted(available_plots, key=lambda xy: self.pyth(xy, owner.home.location))
        else:
            np.random.shuffle(available_plots)

        if len(available_plots):
            location = available_plots[0]
        else:
            location = None

        return location

    def find_sized_property(self, zone, xsize, ysize, owner=None):
        zone_map = self.getZoningMap()
        # print(np.lib.stride_tricks.sliding_window_view(zone_map==zone, (xsize, ysize)).all(axis=(-2,-1)))
        available_plots = np.argwhere(np.lib.stride_tricks.sliding_window_view(zone_map==zone, (xsize, ysize)).all(axis=(-2,-1)))
        if owner:
            available_plots = sorted(available_plots, key=lambda xy: self.pyth(xy, owner.home.location))
        else:
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

    # TODO-DONE should show * every 5 plots on header and sidebar
    def get_print_map(self):
        print_map = ""

        # Add navigational guides to map (longitude)
        star_row = " *   " * ((self.local_map.shape[0] // 5) + 1)
        print_map += star_row + "\n"

        for k, row in enumerate(self.local_map):
            # Lines of latitude
            lat = "*" if not k % 5 else " "
            rowAppearance = lat
            
            for i in row:
                if (i == None):
                    rowAppearance = rowAppearance + "_"
                elif i == "r":
                    rowAppearance = rowAppearance + "r"
                elif i == "b":
                    rowAppearance = rowAppearance + "b"
                else:
                    rowAppearance = rowAppearance + i.character
            
            print_map += rowAppearance + lat + "\n"

        # Bottom lines of longitude
        print_map += star_row

        return print_map

    def get_zoning_print_map(self):
        """Generates a printable map of the locality's zoning."""
        print_map = ""

        # Add navigational guides to map (longitude)
        star_row = " *   " * ((self.zoning_map.shape[0] // 5) + 1)
        print_map += star_row + "\n"

        for k, row in enumerate(self.zoning_map):
            # Lines of latitude
            lat = "*" if not k % 5 else " "
            rowAppearance = lat

            for x in row:
                rowAppearance = rowAppearance + x

            print_map += rowAppearance + lat + "\n"

        # Bottom lines of longitude
        print_map += star_row

        return print_map

    def getDayNum(self):
        return self.model.getDayNum()

    def date(self):
        return self.model.calendar.date()
