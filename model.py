import database as d
import clock as cl
import ai
import generator
import unit as u
from gui import gui

class Model(object):

    def __init__(self):
        self.clock          = cl.Clock(self)
        self.week           = cl.Week(self)
        self.calendar       = cl.SecularCalendar()
        self.productionAI   = ai.ProductionAI(self)
        self.jobPoster      = ai.JobPoster(self)
        self.hirer          = ai.Hirer(self)
        self.firer          = ai.Firer(self)
        self.startupAI      = ai.StartupAI()
        self.builder        = ai.Builder(self)
        self.salaryPayer    = ai.SalaryPayer(self)
        ourGen              = generator.generator(self)
        self.ourWorld       = ourGen.generateWorld(10000, 10, 10)
        Jonestown           = d.getLocality()[0]
        yourHome            = u.House(Jonestown, (3,5))
        self.char           = ai.Character(self, "John Doe", 0, 18, Jonestown, yourHome, [0,0], d.getReligions()[0])
        ourGen.makeFriends()
        self.gui            = gui.gui(self.char)
        # self.gui.mainloop()

    def out(self, text):
        self.gui.out(text)

    def getCharBusinesses(self):
        return self.char.getBusinesses()

    def getDayNum(self):
        return self.clock.getDayNum()