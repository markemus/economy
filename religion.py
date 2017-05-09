import database as d
import clock
from transitions import Machine
from transitions import State

class Religion(object):

    def __init__(self, reliName, months, daysPerMonth, firstMonth, year):
        self.name = reliName
        self.businesses = []
        self.calendar = clock.Calendar(months, daysPerMonth, firstMonth, year)
        d.addReligion(self)

    def addBusiness(self, business):
        self.businesses.append(business)

    def getBusinesses(self):
        return self.businesses

    def getJobs(self):  
        return self.jobList

    def addJob(self, job):
        self.jobList.append(job)

    def getSongs(self):
        return self.songs

class Catholicism(Religion):
    months = [State(name='January', on_enter=['yearChange']),'February','March','April','May','June','July','August','September','October','November','December']
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1000

    def __init__(self):
        Religion.__init__(self, "Catholic", Catholicism.months, Catholicism.daysPerMonth, 'January', Catholicism.year)
        self.songs = [
        "In Paradisum (Fauré)",
        "Crux Fidelis (Saint Venantius Fortunatus)",
        "Beautiful Savior/Crusader's Hymn (anonymous)",
        "Domine Jesu Christe (Mozart)"]


class Protestantism(Religion):
    months = [State(name='January', on_enter=['yearChange']),'February','March','April','May','June','July','August','September','October','November','December']
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1000

    def __init__(self):
        Religion.__init__(self, "Catholic", Protestantism.months, Protestantism.daysPerMonth, 'January', Protestantism.year)
        self.songs = [
        'Babylon is Fallen (Sacred Harp 117)',
        'Antioch (Sacred Harp 277)',
        'Idumea (Sacred Harp 47b)',
        'Hallelujah (Sacred Harp 146)']