import database as d
import numpy as np
import random
from transitions import Machine

#Conversations are markov chains. Works as follows: a column vector for each CURRENT state j, a row vector for each TARGET state i.
#Each entry i,j = the probability of moving to state i from state j.
#target state D = end of conversation. We start in state D when initializing conversation.
#row vectors sum to 1, internal lists are columns.

#Conversation is a singleton. DO NOT CREATE NEW CONVERSATION OBJECTS.
class Conversation(object):
    #a. stores, b.manufacturers, c.friends, d. myself, e.end conversation
    topicMatrix = [
    [0.00,0.45,0.25,0.25,0],
    [0.45,0.00,0.25,0.25,0],
    [0.15,0.15,0.00,0.25,0],
    [0.15,0.15,0.25,0.00,1.0],
    [0.25,0.25,0.25,0.25,0]
    ]

    topicMatrix = [
    [0.00,0.45,0.25,0.25,0],
    [0.45,0.00,0.25,0.25,0],
    [0.15,0.15,0.00,0.25,0],
    [0.15,0.15,0.25,0.00,1.0],
    [0.25,0.25,0.25,0.25,0]
    ]

    #a. different store, b. new topic, c. end convo, d. prices
    storeMatrix = [
    [0.0,0.0,0.25,0.4],
    [0.0,0.0,0.25,0.4],
    [0.0,0.0,0.25,0.0],
    [1.0,1.0,0.25,0.2]
    ]

    #a. different manufacturer, b. new topic, c. end convo, d. prices
    manuMatrix = [
    [0.0,0.0,0.25,0.3],
    [0.0,0.0,0.25,0.3],
    [0.0,0.0,0.25,0.2],
    [1.0,1.0,0.25,0.2]
    ]

    #a. different friend, b. new topic, c. end convo, d. family, e. job, f. skills
    friendMatrix = [
    [0.00,0.00,0.15,0.10,0.10,0.10],
    [0.00,0.00,0.15,0.10,0.10,0.10],
    [0.00,0.00,0.15,0.10,0.10,0.10],
    [0.34,0.34,0.15,0.00,0.35,0.35],
    [0.33,0.33,0.15,0.35,0.00,0.35],
    [0.33,0.33,0.25,0.35,0.35,0.00]
    ]

    #a. introduction, b. new topic, c. end convo, d. myfamily, e. myjob, f. myskills
    myselfMatrix = [
    [0.0,0,0.15,0.00,0.00,0.00],
    [0.2,0,0.15,0.25,0.25,0.25],
    [0.2,0,0.15,0.25,0.25,0.25],
    [0.2,0,0.15,0.00,0.25,0.25],
    [0.2,1,0.15,0.25,0.00,0.25],
    [0.2,0,0.15,0.25,0.25,0.00]
    ]

    states = ['topic','store','manu','friend', 'myself', 'exit']

    transitions = [
    {'trigger' : 'toTopic',   'source' : '*',     'dest' : 'topic'},
    {'trigger' : 'toStore',   'source' : 'topic', 'dest' : 'store'},
    {'trigger' : 'toManu' ,   'source' : 'topic', 'dest' : 'manu' },
    {'trigger' : 'toFriend',  'source' : 'topic', 'dest' : 'friend' },
    {'trigger' : 'toMyself',  'source' : 'topic', 'dest' : 'myself'},
    {'trigger' : 'toExit',    'source' : '*',     'dest' : 'exit'}
    ]

    def __init__(self):
        self.isPlayer = False
        self.firstPerson = None
        self.secondPerson = None
        self.target = None
        self.machine  = Machine(model=self, states=Conversation.states, transitions=Conversation.transitions, initial='exit')
        self.menuDict = {
            'topic'  : [self.toStore, self.toManu, self.toFriend, self.toMyself, self.toExit],
            'store'  : [self.different, self.toTopic, self.toExit, self.prices],
            'manu'   : [self.different, self.toTopic, self.toExit, self.prices],
            'friend' : [self.different, self.toTopic, self.toExit, self.family, self.job, self.skills],
            'myself' : [self.introduction, self.toTopic, self.toExit, self.myfamily, self.myjob, self.myskills]
            }
        self.machine.on_enter_topic('topicHandler')
        self.machine.on_enter_store('storeHandler')
        self.machine.on_enter_manu('manuHandler')
        self.machine.on_enter_friend('friendHandler')
        self.machine.on_enter_myself('myselfHandler')
        self.machine.on_enter_exit('exitHandler')

    def beginConversation(self, firstPerson, secondPerson, isPlayer=False):
        self.isPlayer = isPlayer
        self.firstPerson = firstPerson
        self.secondPerson = secondPerson
        self.introduction()
        self.toTopic()

    def introduction(self):
        self.firstPerson.peopleManager(self.secondPerson)
        self.secondPerson.peopleManager(self.firstPerson)

    def different(self):
        if self.state == 'friend':
            testTarget = self.firstPerson.randomPerson(self.target)
            if testTarget is not None:
                self.target = testTarget.person
            else:
                self.target = None

        elif self.state == 'manu':
            testTarget = self.firstPerson.randomManu(self.target)
            if testTarget is not None:
                self.target = testTarget.store
            else:
                self.target = None

        elif self.state == 'store':
            testTarget = self.firstPerson.randomStore(self.target)
            if testTarget is not None:
                self.target = testTarget.store
            else:
                self.target = None

    def prices(self):
        if self.target is not None:
            # if self.state == 'store':
            #     firstProfile  = self.firstPerson.storeManager(self.target)
            #     secondProfile = self.secondPerson.storeManager(self.target)

            # elif self.state == 'manu':
            firstProfile  = self.firstPerson.unitManager(self.target)
            secondProfile = self.secondPerson.unitManager(self.target)

            firstPrices  = firstProfile.getPricesWithDayNum()
            secondPrices = secondProfile.getPricesWithDayNum()
            firstDayNum  = firstPrices[1]
            secondDayNum = secondPrices[1]

            if firstDayNum > secondDayNum:
                prices = firstPrices[0]
                secondProfile.updatePrices(prices, firstDayNum)
                #thoughts
                self.firstPerson.think("I told " + self.secondPerson.name + " about " + self.target.name + "'s new prices.")
                self.secondPerson.think(self.firstPerson.name + " told me about " + self.target.name + "'s new prices.")

            elif secondDayNum > firstDayNum:
                prices = secondPrices[0]
                firstProfile.updatePrices(prices, secondDayNum)
                #thoughts
                self.firstPerson.think(self.secondPerson.name + " told me about " + self.target.name + "'s new prices.")
                self.secondPerson.think("I told " + self.firstPerson.name + " about " + self.target.name + "'s new prices.")

            else:
                self.firstPerson.think(self.secondPerson.name + " and I talked about " + self.target.name + "'s prices.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about " + self.target.name + "'s prices.")
        else:
            if self.state == 'store':
                self.firstPerson.think(self.secondPerson.name + " and I talked about how weird it is that there are no stores in the area.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about how weird it is that there are no stores in the area.")
            elif self.state == 'manu':
                self.firstPerson.think(self.secondPerson.name + " and I talked about how weird it is that there are no manufacturers in the area.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about how weird it is that there are no manufacturers in the area.")
            else:
                self.firstPerson.think("There is a bug in conversation.prices.")
                self.secondPerson.think("There is a bug in conversation.prices.")

    def family(self):
        None

    def job(self):
        if self.target is not None:
            firstProfile = self.firstPerson.peopleManager(self.target)
            secondProfile = self.secondPerson.peopleManager(self.target)

            firstJob  = firstProfile.getJob()
            secondJob = secondProfile.getJob()
            firstDayNum  = firstJob[1]
            secondDayNum = secondJob[1]

            if firstDayNum > secondDayNum:
                job = firstJob[0]
                secondProfile.updateJob(job, firstDayNum)
                #thoughts
                self.firstPerson.think("I told " + self.secondPerson.name + " about " + self.target.name + "'s new job.")
                self.secondPerson.think(self.firstPerson.name + " told me about " + self.target.name + "'s new job.")

            elif secondDayNum > firstDayNum:
                job = secondJob[0]
                firstProfile.updateJob(job, secondDayNum)
                #thoughts
                self.firstPerson.think(self.secondPerson.name + " told me about " + self.target.name + "'s new job.")
                self.secondPerson.think("I told " + self.firstPerson.name + " about " + self.target.name + "'s new job.")

            else:
                self.firstPerson.think(self.secondPerson.name + " and I talked about " + self.target.name + "'s job.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about " + self.target.name + "'s job.")
        else:
            self.firstPerson.think("I need to make more friends.")
            self.secondPerson.think("I need to make more friends.")

    def skills(self):
        None

    def myfamily(self):
        pass

    def myjob(self):
        #info: jobs, jobUnits, *salaries
        #profiles
        firstProfile = self.secondPerson.peopleManager(self.firstPerson)
        secondProfile = self.firstPerson.peopleManager(self.secondPerson)

        #variables
        firstJob = self.firstPerson.getJob()
        secondJob = self.secondPerson.getJob()

        try:
            firstJobType = firstJob.getJobType()
            firstJobUnit = firstJob.getUnit()
            firstJobLoc = firstJobUnit.getName()
        except:
            firstJobType = "Jobhunter"
            firstJobUnit = None
            firstJobLoc = "home"        
        
        try:
            secondJobType = secondJob.getJobType()
            secondJobUnit = secondJob.getUnit()
            secondJobLoc = secondJobUnit.getName()
        except:
            secondJobType = "Jobhunter"
            secondJobUnit = None
            secondJobLoc = "home"

        dayNum = self.firstPerson.model.getDayNum()

        #update profiles
        firstProfile.updateJob(firstJob, dayNum)
        # firstProfile.updateSalary(salaryRange, dayNum)
        secondProfile.updateJob(secondJob, dayNum)
        # secondProfile.updateSalary(salaryRange, dayNum)

        if firstJobUnit is not None:
            self.secondPerson.unitManager(firstJobUnit)
        if secondJobUnit is not None:
            self.firstPerson.unitManager(secondJobUnit)       

        #thoughts
        self.firstPerson.think(self.secondPerson.name + " told me about their job as a " + secondJobType + " at " + secondJobLoc + ".")
        self.secondPerson.think(self.firstPerson.name + " told me about their job as a " + firstJobType + " at " + firstJobLoc + ".")

    def myskills(self):
        pass

    #dialogues are chosen here, but the actual method call is in the handler (eg prices)
    def talk(self, matrix, stateVector):

        if self.isPlayer:
            # stateVector = playerChoice
            pass
        else:
            #get dialogue probabilities given last dialogue
            probArray = np.dot(matrix, stateVector)
            prob = probArray.tolist()

            #choose dialogue
            choice = random.random()
            stateVector = [0 for i in range(len(prob))]
            
            for i in range(len(prob)):
                outcome = prob[i]

                if outcome >= choice:
                    stateVector[i] = 1
                    return stateVector
                else:
                    choice = choice - outcome

    def topicHandler(self):
        matrix = Conversation.topicMatrix
        stateVector = [0,0,0,0,1]
        self.firstPerson.think("topicHandler")

        stateVector = self.talk(matrix, stateVector)
        for i in range(len(stateVector)):
            if stateVector[i] == 1:
                self.menuDict[self.state][i]()
                break

    def storeHandler(self):
        matrix = Conversation.storeMatrix
        stateVector = [0,1,0,0]
        self.firstPerson.think("storeHandler")

        self.different()

        while self.state == 'store':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def manuHandler(self):
        matrix = Conversation.manuMatrix
        stateVector = [0,1,0,0]
        self.firstPerson.think("manuHandler")

        self.different()

        while self.state == 'manu':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def friendHandler(self):
        matrix = Conversation.friendMatrix
        stateVector = [0,1,0,0,0,0]
        self.firstPerson.think("friendHandler")
        
        self.different()

        while self.state == 'friend':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def myselfHandler(self):
        matrix = Conversation.myselfMatrix
        stateVector = [0,1,0,0,0,0]
        self.firstPerson.think("myselfHandler")

        while self.state == 'myself':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def exitHandler(self):
        self.isPlayer = False

Convo = Conversation()