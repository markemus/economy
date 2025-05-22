import database as d
import clock
# from transitions import State


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
    year = 1600

    def __init__(self):
        Religion.__init__(self, "Catholic", Catholicism.months, Catholicism.daysPerMonth, "January", Catholicism.year)
        self.songs = [
            "Ave Maria",
            "Pange Lingua Gloriosi (Saint Thomas Aquinas)",
            "Dona Nobis Pacem",
            "Ave Verum Corpus (Pope Innocent)",
            "Gloria in Excelsis Deo (Hilary of Poitiers)",
            "In Paradisum (Fauré)",
            "Crux Fidelis (Saint Venantius Fortunatus)",
            "Crusader's Hymn (anonymous)",
            "Domine Jesu Christe"]
        self.churchNames = [
            "Blessed Mother Cathedral",
            "Cathedral Basilica of the Immaculate Conception",
            "Most Pure Heart of Mary Catholic Church",
            "St Joseph's Roman Catholic Church",
            "Cathedral of St Paul",
            "Sacred Heart Catholic Church",
            "Holy Family Old Cathedral",
            "St Mary's Church",
            "Our Lady of the Blessed Sacrament Church",
            "Our Lady of Victory Church",
            "Cathedral of St Augustine",
            "Immaculate Heart of Mary Church",
            "Old Santa Rosa Catholic Church",
            "Catholic Church of the Assumption",
            "Cathedral of Our Lady of the Angels",
            "Precious Blood Church",
            "Cathedral of Christ the Light",
            "Cathedral of the Annunciation"]


class Protestantism(Religion):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = 1600

    def __init__(self):
        Religion.__init__(self, "Catholic", Protestantism.months, Protestantism.daysPerMonth, "January", Protestantism.year)
        self.songs = [
            "Onward Christian Soldiers (Sabine Baring-Gould)",
            "Amazing Grace (John Newton)",
            "Old Rugged Cross (George Bennard)",
            "I Love To Tell the Story (Katherine Hankey)",
            "It Is Well With My Soul (Horatio Spafford)",
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
            "St Mark's Lutheran Church",
            "Sanctuary of Light",
            "Living Waters Church",
            "Covenant Grace Church",
            "Abundant Life Church",
            "Promise Keepers Church",
            "Radiant Life Fellowship"
            "True Vine Fellowship"]
