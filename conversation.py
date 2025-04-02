import database as d
import numpy as np
import random
from transitions import Machine

# Conversations are markov chains. Works as follows: a column vector for each CURRENT state j, a row vector for each TARGET state i.
# Each entry i,j = the probability of moving to state i from state j.
# target state D = end of conversation. We start in state D when initializing conversation.
# row vectors sum to 1, internal lists are columns.

# Conversation is a singleton. DO NOT CREATE NEW CONVERSATION OBJECTS.
class Conversation(object):
    #a. stores, b.manufacturers, c.friends, d. myself, e.end conversation

    topicMatrix = [
    [0.00,0.20,0.15,0.15,0.25],
    [0.20,0.00,0.15,0.15,0.25],
    [0.15,0.15,0.00,0.20,0.25],
    [0.15,0.15,0.20,0.00,0.25],
    [0.50,0.50,0.50,0.50,0.00]
    ]

    #a. different store, b. new topic, c. end convo, d. prices
    storeMatrix = [
    [0.0,0.0,0.25,0.25],
    [0.0,0.0,0.25,0.25],
    [0.0,0.0,0.25,0.50],
    [1.0,1.0,0.25,0.00]
    ]

    #a. different manufacturer, b. new topic, c. end convo, d. prices
    manuMatrix = [
    [0.0,0.0,0.25,0.25],
    [0.0,0.0,0.25,0.25],
    [0.0,0.0,0.25,0.50],
    [1.0,1.0,0.25,0.00]
    ]

    #a. different friend, b. new topic, c. end convo, d. family, e. job, /f. skills
    friendMatrix = [
    [0.0,0.0,0.2,0.1,0.1],
    [0.0,0.0,0.2,0.2,0.2],
    [0.0,0.0,0.2,0.5,0.5],
    [0.5,0.5,0.2,0.0,0.2],
    [0.5,0.5,0.2,0.2,0.0]
    ]
    # friendMatrix = [
    # [0.00,0.00,0.15,0.1,0.1,0.1],
    # [0.00,0.00,0.15,0.2,0.2,0.2],
    # [0.00,0.00,0.15,0.5,0.5,0.5],
    # [0.34,0.34,0.15,0.0,0.1,0.1],
    # [0.33,0.33,0.15,0.1,0.0,0.1],
    # [0.33,0.33,0.25,0.1,0.1,0.0]
    # ]

    #a. introduction, b. new topic, c. end convo, d. myfamily, e. myjob, /f. myskills
    myselfMatrix = [
    [0.00,1,0.2,0.0,0.0],
    [0.25,0,0.2,0.2,0.2],
    [0.25,0,0.2,0.5,0.5],
    [0.25,0,0.2,0.0,0.3],
    [0.25,0,0.2,0.3,0.0]
    ]
    # myselfMatrix = [
    # [0.0,1,0.15,0.00,0.00,0.00],
    # [0.2,0,0.15,0.20,0.20,0.20],
    # [0.2,0,0.15,0.50,0.50,0.50],
    # [0.2,0,0.15,0.00,0.15,0.15],
    # [0.2,0,0.15,0.15,0.00,0.15],
    # [0.2,0,0.15,0.15,0.15,0.00]
    # ]

    states = ['topic', 'store', 'manu', 'friend', 'myself', 'exit']

    transitions = [
        {'trigger': 'toTopic',   'source': '*',     'dest': 'topic'},
        {'trigger': 'toStore',   'source': 'topic', 'dest': 'store'},
        {'trigger': 'toManu' ,   'source': 'topic', 'dest': 'manu'},
        {'trigger': 'toFriend',  'source': 'topic', 'dest': 'friend'},
        {'trigger': 'toMyself',  'source': 'topic', 'dest': 'myself'},
        {'trigger': 'toExit',    'source': '*',     'dest': 'exit'}
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
            'friend' : [self.different, self.toTopic, self.toExit, self.family, self.job],
            'myself' : [self.introduction, self.toTopic, self.toExit, self.myfamily, self.myjob]
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
        p2 = self.firstPerson.peopleManager(self.secondPerson)
        p1 = self.secondPerson.peopleManager(self.firstPerson)

        p2.name = self.secondPerson.name
        p1.name = self.firstPerson.name

        p2.updateOpinion(1)
        p1.updateOpinion(1)

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
            # TODO people should prefer stores they like (high experience)
            testTarget = self.firstPerson.randomStore(self.target)
            if testTarget is not None:
                self.target = testTarget.store
            else:
                self.target = None

    def prices(self):
        if self.target is not None:
            firstProfile  = self.firstPerson.unitManager(self.target, self.secondPerson)
            secondProfile = self.secondPerson.unitManager(self.target, self.firstPerson)

            firstPrices  = firstProfile.getPricesWithDayNum()
            secondPrices = secondProfile.getPricesWithDayNum()
            firstDayNum  = firstPrices[1]
            secondDayNum = secondPrices[1]

            if firstDayNum > secondDayNum:
                prices = firstPrices[0]
                secondProfile.updatePrices(prices, firstDayNum)
                #thoughts
                self.firstPerson.think("I told " + self.secondPerson.name + " about the prices at " + self.target.name + ".")
                self.secondPerson.think(self.firstPerson.name + " told me about the prices at " + self.target.name + ".")

            elif secondDayNum > firstDayNum:
                prices = secondPrices[0]
                firstProfile.updatePrices(prices, secondDayNum)
                #thoughts
                self.firstPerson.think(self.secondPerson.name + " told me about the prices at " + self.target.name + ".")
                self.secondPerson.think("I told " + self.firstPerson.name + " about the prices at " + self.target.name + ".")

            else:
                self.firstPerson.think(self.secondPerson.name + " and I talked about " + self.target.name + "'s prices.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about " + self.target.name + "'s prices.")
        else:
            if self.state == 'store':
                self.firstPerson.think(self.secondPerson.name + " listened to me gripe about how I can't find anywhere to shop.")
                self.secondPerson.think(self.firstPerson.name + " told me that they can't find anywhere to shop.")
            elif self.state == 'manu':
                self.firstPerson.think("I mentioned to " + self.secondPerson.name + " that I don't know anything about the local industry.")
                self.secondPerson.think(self.firstPerson.name + " told me that they don't know much about the local industry.")
            # else:
            #     self.firstPerson.think("There is a bug in conversation.prices. (not manu or store)")
            #     self.secondPerson.think("There is a bug in conversation.prices. (not manu or store)")


    def family(self):
        if self.target is not None:
            # info: family, people
            # profiles
            p1 = self.firstPerson.peopleManager(self.target)
            p2 = self.secondPerson.peopleManager(self.target)

            # variables
            f1 = p1.getFamily()
            f2 = p2.getFamily()
            ff = []

            # update profiles
            for a, b in zip(f1, f2):
                if a[-1] >= b[-1]:
                    ff.append(a)
                else:
                    ff.append(b)

            p1.updateFamily(*ff)
            p2.updateFamily(*ff)

            # thoughts
            self.firstPerson.think(self.secondPerson.name + " and I gossiped about " + self.target.name + "'s family.")
            self.secondPerson.think(self.firstPerson.name + " and I gossiped about " + self.target.name + "'s family.")

        else:
            self.firstPerson.think("I don't really know anything about my friends' families.")
            self.secondPerson.think("I don't really know anything about my friends' families.")

    def job(self):
        if self.target is not None:
            # profiles
            firstProfile = self.firstPerson.peopleManager(self.target)
            secondProfile = self.secondPerson.peopleManager(self.target)

            # variables
            firstJob  = firstProfile.getJob()
            secondJob = secondProfile.getJob()

            # update profiles
            if firstJob[1] > secondJob[1]:
                secondProfile.updateJob(*firstJob)
                self.firstPerson.think("I told " + self.secondPerson.name + " what " + self.target.name + " does for a living.")
                self.secondPerson.think(self.firstPerson.name + " told me what " + self.target.name + " does for a living.")

            elif secondJob[1] > firstJob[1]:
                firstProfile.updateJob(*secondJob)
                self.firstPerson.think(self.secondPerson.name + " told me what " + self.target.name + " does for a living.")
                self.secondPerson.think("I told " + self.firstPerson.name + " about " + self.target.name + " does for a living.")

            else:
                self.firstPerson.think(self.secondPerson.name + " and I talked about " + self.target.name + "'s job.")
                self.secondPerson.think(self.firstPerson.name + " and I talked about " + self.target.name + "'s job.")
        else:
            self.firstPerson.think("I don't know what any of my friends do for a living!")
            self.secondPerson.think("I don't know what any of my friends do for a living!")

    # def skills(self):
    #     #info: skills
    #     if self.target is not None:
    #         #profiles
    #         firstProfile = self.firstPerson.peopleManager(self.target)
    #         secondProfile = self.secondPerson.peopleManager(self.target)

    #         #variables
    #         firstSkills = firstProfile.getSkills()
    #         secondSkills = secondProfile.getSkills()

    #         #update profiles
    #         if firstSkills[1] > secondSkills[1]:
    #             secondProfile.updateSkills(*firstSkills)
    #             self.firstPerson.think("I told " + self.secondPerson.name + " about how good " + self.target.name + " is with their hands.")
    #             self.secondPerson.think(self.firstPerson.name + " told me about how good " + self.target.name + " is with their hands.")

    #         elif secondSkills[1] > firstSkills[1]:
    #             firstProfile.updateSkills(*secondSkills)
    #             self.firstPerson.think(self.secondPerson.name + " told me about how good " + self.target.name + " is with their hands.")
    #             self.secondPerson.think("I told " + self.firstPerson.name + " about how good " + self.target.name + " is with their hands.")

    #         else:
    #             self.firstPerson.think(self.secondPerson.name + " and I talked about how good " + self.target.name + " is with their hands.")
    #             self.secondPerson.think(self.firstPerson.name + " and I talked about how good " + self.target.name + " is with their hands.")

    #     else:
    #         self.firstPerson.think("I should spend more time doing things with my friends.")
    #         self.secondPerson.think("I should spend more time doing things with my friends.")

    def myfamily(self):
        # info: family, people
        # profiles
        firstProfile = self.secondPerson.peopleManager(self.firstPerson)
        secondProfile = self.firstPerson.peopleManager(self.secondPerson)

        firstOwn = self.firstPerson.peopleManager(self.firstPerson)
        secondOwn = self.secondPerson.peopleManager(self.secondPerson)

        # update profiles
        firstProfile.updateFamily(firstOwn.getFather(), firstOwn.getMother(), firstOwn.getSpouse(), firstOwn.getSiblings(), firstOwn.getChildren())
        secondProfile.updateFamily(secondOwn.getFather(), secondOwn.getMother(), secondOwn.getSpouse(), secondOwn.getSiblings(), secondOwn.getChildren())

        # thoughts
        self.firstPerson.think(self.secondPerson.name + " caught me up on their family life.")
        self.secondPerson.think(self.firstPerson.name + " caught me up on their family life.")
        
    def myjob(self):
        # info: jobs, jobUnits, *salaries
        # profiles
        firstProfile = self.secondPerson.peopleManager(self.firstPerson)
        secondProfile = self.firstPerson.peopleManager(self.secondPerson)

        # variables
        firstJob = self.firstPerson.getJob()
        secondJob = self.secondPerson.getJob()
        dayNum = self.firstPerson.model.getDayNum()

        try:
            firstJobType = firstJob.getJobType()
            firstJobUnit = firstJob.getUnit()
            firstJobLoc = firstJobUnit.getName()
            firstSalary = firstJob.getSalary()
        except:
            firstJobType = "Jobhunter"
            firstJobUnit = None
            firstJobLoc = "home"        
            firstSalary = 0
        
        try:
            secondJobType = secondJob.getJobType()
            secondJobUnit = secondJob.getUnit()
            secondJobLoc = secondJobUnit.getName()
            secondSalary = secondJob.getSalary()
        except:
            secondJobType = "Jobhunter"
            secondJobUnit = None
            secondJobLoc = "home"
            secondSalary = 0


        # update profiles
        if dayNum > firstProfile.getJob()[1]:
            firstProfile.updateJob(firstJob, dayNum)
        if dayNum > firstProfile.getSalary()[1]:
            firstProfile.updateSalary(firstSalary, dayNum)
        
        if dayNum > secondProfile.getJob()[1]:
            secondProfile.updateJob(secondJob, dayNum)
        if dayNum > secondProfile.getSalary()[1]:
            secondProfile.updateSalary(firstSalary, dayNum)

        if firstJobUnit is not None:
            self.secondPerson.unitManager(firstJobUnit, self.firstPerson)
        if secondJobUnit is not None:
            self.firstPerson.unitManager(secondJobUnit, self.secondPerson)

        # thoughts
        self.firstPerson.think(self.secondPerson.name + " told me about their job as a " + secondJobType + " at " + secondJobLoc + ".")
        self.secondPerson.think(self.firstPerson.name + " told me about their job as a " + firstJobType + " at " + firstJobLoc + ".")

    # def myskills(self):
    #     #info skills
    #     #profiles
    #     firstProfile = self.secondPerson.peopleManager(self.firstPerson)
    #     secondProfile = self.firstPerson.peopleManager(self.secondPerson)

    #     #variables
    #     firstSkills = self.firstPerson.getSkills()
    #     secondSkills = self.secondPerson.getSkills()
    #     dayNum = self.firstPerson.model.getDayNum()

    #     #update profiles
    #     if dayNum > firstProfile.getSkills()[1]:
    #         firstProfile.updateSkills(firstSkills, dayNum)
    #     if dayNum > secondProfile.getSkills()[1]:
    #         secondProfile.updateSkills(secondSkills, dayNum)

    #     #thoughts
    #     self.firstPerson.think(self.secondPerson.name + " and I talked shop for a while.")
    #     self.secondPerson.think(self.firstPerson.name + " and I talked shop for a while.")

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
        # self.firstPerson.think("topicHandler")

        stateVector = self.talk(matrix, stateVector)
        for i in range(len(stateVector)):
            if stateVector[i] == 1:
                self.menuDict[self.state][i]()
                break

    def storeHandler(self):
        matrix = Conversation.storeMatrix
        stateVector = [0,1,0,0]
        # self.firstPerson.think("storeHandler")

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
        # self.firstPerson.think("manuHandler")

        self.different()

        while self.state == 'manu':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def friendHandler(self):
        matrix = Conversation.friendMatrix
        stateVector = [0,1,0,0,0]
        # self.firstPerson.think("friendHandler")
        
        self.different()

        while self.state == 'friend':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def myselfHandler(self):
        matrix = Conversation.myselfMatrix
        stateVector = [0,1,0,0,0]
        # self.firstPerson.think("myselfHandler")

        while self.state == 'myself':
            stateVector = self.talk(matrix, stateVector)
            for i in range(len(stateVector)):
                if stateVector[i] == 1:
                    self.menuDict[self.state][i]()
                    break

    def exitHandler(self):
        self.isPlayer = False


Convo = Conversation()
