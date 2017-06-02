import jobs as j

class manu_staff(object):

    def __init__(self, unit):
        self.unit = unit
        self.manager = j.Manager(unit.getBusiness(), unit, 40)
        self.carrier = j.Carrier(1, unit.getBusiness(), unit, 40)
        



class church_staff(object):

    def __init__(self, unit):
        self.unit = unit
        self.manager = j.Manager(unit.getBusiness(), unit, 40)
        self.carrier = j.Carrier(1, unit.getBusiness(), unit, 40)
        self.priests = j.Priest(1, unit.getBusiness(), unit, 40)