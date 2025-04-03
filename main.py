import random
import copy
import cProfile

import ai
import business as b
import database as d
import gameMap as g
import generator as gen
import jobs as j
import orders as o
import people as p
import profiles as pr
import unit as u

from conversation import Convo
from gui import gui
from model import Model


# main
model = Model()
Jonestown = d.getLocality()[0]
model.week.machine.set_state("Monday")

# players
you = model.gui.char

CatholicChurch = d.getChurches()[0]
ProtestantChurch  = d.getChurches()[1]

# testbus
testBus = you.startBusiness("Williamson Shipping LTD")
testBus.cash = 1000000

# TODO-DECIDE add public domain music?
# TODO debug hiring. Should be slow to add new hires (and buyers should be more forgiving for low stocks)
# TODO currently bakeries run out of raw supplies after 30ish days.
d.addBoss(you)

# for day in range(30):
#     model.clock.runDay()

# TODO-NOTE run with -i flag and hit "quit" once to access terminal.
model.gui.mainloop()
