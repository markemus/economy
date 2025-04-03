import database as d
import clock
from transitions import State


class Religion:
    def __init__(self, reliName, months, daysPerMonth, firstMonth, year):
        self.name = reliName
        self.businesses = []
        self.calendar = clock.Calendar(months, daysPerMonth, firstMonth, year)
        d.addReligion(self)

    def addBusiness(self, business):
        self.businesses.append(business)

    def getBusinesses(self):
        return self.businesses

    def getLocalBusiness(self, locality):
        for business in self.businesses:
            if business.locality == locality:
                return business
        return None

    def getJobs(self):  
        return self.jobList

    def addJob(self, job):
        self.jobList.append(job)

    def getSongs(self):
        return self.songs


# TODO add more songs and church names.
# TODO religious holidays
class Catholicism(Religion):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1000

    def __init__(self):
        Religion.__init__(self, "Catholic", Catholicism.months, Catholicism.daysPerMonth, "January", Catholicism.year)
        self.songs = [
        "In Paradisum (Fauré)",
        "Crux Fidelis (Saint Venantius Fortunatus)",
        "Crusader's Hymn (anonymous)",
        "Domine Jesu Christe (Mozart)"]
        self.churchNames = [
        "Blessed Mother Cathedral", 
        "Cathedral Basilica of the Immaculate Conception",
        "Most Pure Heart of Mary Catholic Church",
        "St Joseph's Roman Catholic Church"]


class Protestantism(Religion):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1000

    def __init__(self):
        Religion.__init__(self, "Catholic", Protestantism.months, Protestantism.daysPerMonth, "January", Protestantism.year)
        self.songs = [
        "Babylon is Fallen (Sacred Harp 117)",
        "Antioch (Sacred Harp 277)",
        "Idumea (Sacred Harp 47b)",
        "Hallelujah (Sacred Harp 146)",
        "Soar Away (Sacred Harp 455)",
        "I'm Going Home (Sacred Harp 282)",
        "Cleansing Fountain (Sacred Harp 505)",
        "Nearer My God to Thee (Sacred Harp 488b)"]
        self.churchNames = [
        "Holy Spirit Ministry",
        "Emmanuel House of Prayer",
        "Lloyd Street Church",
        "St Mark's Lutheran Church"]
