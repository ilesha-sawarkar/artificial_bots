#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random
import constants as c
from simulation import SIMULATION
import sys

print(sys.argv)
directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
print(solutionID)

simulation = SIMULATION(directOrGUI, solutionID)

#simulation = SIMULATION(directOrGUI)	
simulation.Run()
simulation.Get_Fitness()


#step 57 