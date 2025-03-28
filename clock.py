import database as d
from transitions import Machine
from transitions import State
# from ai import startupAI, productionAI

class Clock(object):
    states = ['work', 'relax', 'shop', 'sleep']

    def __init__(self, model):
        self.dayNumber = -1
        self.model = model
        self.machine = Machine(model=self, states=Clock.states, initial='sleep')
        self.machine.add_ordered_transitions()
        self.machine.on_enter_work('workHandler')
        self.machine.on_enter_relax('relaxHandler')
        self.machine.on_enter_shop('shopHandler')
        self.machine.on_enter_sleep('sleepHandler')

    def next_day(self):
        self.model.week.next_state()
        self.model.calendar.next_day()
        d.shufflePeople()
        self.dayNumber += 1

        # Clear thoughts log once a week.
        if self.model.week.state == 'Monday':
            for person in d.getPeople():
                person.thoughts = []

    def workHandler(self):
        self.next_day()

        religionList    = d.getReligions()
        unitList        = d.getUnit()
        businessList    = d.getBusinesses()
        peopleList      = d.getPeople()
        bossList        = d.getBosses()
        localityList    = d.getLocality()

        if self.model.week.state == 'Friday':
            self.model.salaryPayer.paySalaries()

        # TODO going to church should make people happy
        if self.model.week.state == 'Sunday':
            for person in peopleList:
                person.churchHandler()
            for religion in religionList:
                for business in religion.getBusinesses():
                    for priest in business.getPriestJobs():
                        priest.service()
        # workday
        if self.model.week.state != 'Sunday':
            for business in businessList:
                business.workHandler()
            for person in peopleList:
                person.workHandler()
                person.bossmaker()
            for boss in bossList:
                i_build = self.model.startupAI.whatToBuild(boss)
                self.model.builder.buildChain(boss.businesses[0], i_build)

    def relaxHandler(self):
        bossList = d.getBosses()
        businessList = d.getBusinesses()
        peopleList = d.getPeople()

        if self.model.week.state != 'Sunday':
            for boss in bossList:
                for business in boss.getBusinesses():
                    self.model.productionAI.setProduction(business)
                    for job in business.craftingJobs:
                        self.model.jobPoster.managePositions(job)
            for business in businessList:
                business.restHandler()
        
        for person in peopleList:
            person.restHandler()

    def shopHandler(self):
        businessList = d.getBusinesses()
        peopleList = d.getPeople()

        if self.model.week.state != 'Sunday':
            for business in businessList:
                business.shopHandler()
            for person in peopleList:
                person.shopHandler()

    def sleepHandler(self):
        peopleList      = d.getPeople()
        businessList    = d.getBusinesses()

        for person in peopleList:
            person.sleepHandler()

        if self.model.week.state != 'Sunday':
            for business in businessList:
                business.sleepHandler()
        
        self.model.out("\nThe day ends.\n")

    def toString(self):
        return("Today is " 
            + self.model.week.state 
            + ", " 
            + str(self.model.calendar.dayOfMonth) 
            + " of " 
            + self.model.calendar.state 
            + " in the year " 
            + str(self.model.calendar.year) 
            + "." 
            + " At this time of day people generally " 
            + self.state 
            + "."
            )

    def runDay(self):
        self.next_state()
        self.next_state()
        self.next_state()
        self.next_state()

    def getDayNum(self):
        return self.dayNumber


class Week(object):
    states = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    def __init__(self, model):
        self.model = model
        self.machine = Machine(model=self, states=Week.states, initial='Thursday')
        self.machine.add_ordered_transitions()


# TODO People's thoughts should use their religion's calendar?
class Calendar(object):
    def __init__(self, months, daysPerMonth, firstMonth, year):
        # self.locality = locality
        self.machine = Machine(model=self, states=months, initial=firstMonth)
        self.machine.add_ordered_transitions()
        self.first_month = firstMonth
        self.dayOfMonth = 1

    #should use daysPerMonth
    def next_day(self):
        if self.dayOfMonth == 30:
            self.next_state()
            self.dayOfMonth = 1
        else:
            self.dayOfMonth += 1

    def yearChange(self):
        self.year += 1

    # TODO date should be machine readable.
    def date(self):
        date = self.state + " " + str(self.dayOfMonth) + ", " + str(self.year)
        return date


# example calendar. Also is the secular calendar- each religion has their own.
class SecularCalendar(Calendar):
    months = [State(name='January', on_enter=['yearChange']), 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1000

    def __init__(self):
        Calendar.__init__(self, SecularCalendar.months, SecularCalendar.daysPerMonth, 'September', SecularCalendar.year)
