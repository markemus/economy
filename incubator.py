import database as d

class incubator(object):

    def __init__(self, parent):
        self.parent = parent
        self.grow_days = {"wheat" : 5, "beer" : 10, "wood" : 5}
        self.rot_days = {"wheat" : 5, "beer" : 10, "wood" : 5}
        self.growing = {"wheat" : [], "beer" : [], "wood" : []}
        self.grow_timers = {"wheat" : [], "beer" : [], "wood" : []}
        self.ripe = {"wheat" : [], "beer" : [], "wood" : []}
        self.rot_timers = {"wheat" : [], "beer" : [], "wood" : []}

    def itorzero(self, it):
        value = 0
        if it > 0:
            value = it
        return value

    def plant(self, mat, amount):
        if amount > 0:
            growtime = self.itorzero(self.grow_days[mat] - sum(self.grow_timers[mat]))
            self.growing[mat].append(amount)
            self.grow_timers[mat].append(growtime)

    def ripen(self, mat):
        ready = self.growing[mat][0]
        timer = self.itorzero(self.rot_days[mat] - sum(self.rot_timers[mat]))
        self.ripe[mat].append(ready)
        self.rot_timers[mat].append(timer)
        del self.growing[mat][0]
        del self.grow_timers[mat][0]

    def harvest(self, mat, amount):
        if len(self.ripe[mat]) > 0:
            ready = self.ripe[mat][0]

            if ready > amount:
                self.ripe[mat][0] -= amount

            elif ready == amount:
                del self.ripe[mat][0]
                del self.rot_timers[mat][0]

            elif ready < amount:
                needed = amount - ready
                amount = ready
                del self.ripe[mat][0]
                del self.rot_timers[mat][0]
                amount += self.harvest(mat, needed)
        else:
            amount = 0

        return amount

    def rot(self, mat):
        ready = self.ripe[mat][0]
        del self.ripe[mat][0]
        del self.rot_timers[mat][0]

    def growth_handler(self):
        for mat in self.grow_timers.keys():
            if len(self.grow_timers[mat]) > 0:
                if self.grow_timers[mat][0] == 0:
                    self.ripen(mat)             
                else:
                    self.grow_timers[mat][0] -= 1

    def rot_handler(self):
        for mat in self.rot_timers.keys():
            if len(self.rot_timers[mat]) > 0:
                if self.rot_timers[mat][0] == 0:
                    self.rot(mat)
                else:
                    self.rot_timers[mat][0] -= 1

    def next_day(self):
        self.growth_handler()
        self.rot_handler()

    def getRipe(self, mat):
        return sum(self.ripe[mat])

    def getGrowing(self, mat):
        return sum(self.growing[mat])

    def toString(self):
        string = (self.parent.name + " incubator:\n"
        + "Growing: " + str(self.growing) + "\n"
        + "Grow timers: " + str(self.grow_timers) + "\n"
        + "Ripe: " + str(self.ripe) + "\n"
        + "Rot timers: " + str(self.rot_timers) + "\n")

        return string

# #test

# inc = incubator(None)

# inc.plant("wheat", 50)
# inc.plant("beer", 20)
# inc.next_day()
# inc.next_day()
# inc.plant("wheat", 21)
# inc.plant("beer", 53)
# print("grow_timers: ", inc.grow_timers)
# print("growing: ", inc.growing)
# inc.next_day()
# inc.next_day()
# inc.next_day()
# inc.next_day()
# inc.next_day()
# inc.next_day()
# inc.next_day()
# print("grow_timers: ", inc.grow_timers)
# print("growing: ", inc.growing)
# print("rot_timers: ", inc.rot_timers)
# print("ripe:", inc.ripe)
# print("harvest wheat: ", inc.harvest("wheat", 5))
# print("harvest beer: ", inc.harvest("beer", 5))
# print("ripe:", inc.ripe)