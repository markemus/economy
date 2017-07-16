import random
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

town = g.Locality(None, (0,0), 10, 10,"Town")