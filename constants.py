#!/usr/bin/env python3

#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random


iter=1000 #iteration times

populationSize= 10


targetAngles = np.sin(np.linspace(0, np.pi*2, iter))
#targetAngles= (targetAngles/2)*(np.pi/2)


numberOfGenerations=10
numSensorNeurons=8
numMotorNeurons=7


motorJointRange=0.3

#FrontLeg 
amplitude_FrontLeg= np.pi/3
frequency_FrontLeg=10
phaseOffset_FrontLeg=0
targetAngles_FrontLeg = np.sin(np.linspace(0, np.pi*2, iter))
maxForce_FrontLeg=28


amplitude_BackLeg= np.pi/3
frequency_BackLeg=19
phaseOffset_BackLeg= np.pi/4
targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, iter))
maxForce_BackLeg=35

#FrontLeg 

'''
iter=1000 #iteration times
am={}
f={}
p={}
F={}

#backleg
am[0] = 1*np.pi/4         # amplitude of backleg
f[0] = 2*np.pi/iter*10    # frequency of backleg
p[0] = 0                     # phaseOffset of backleg
F[0] = 22                   # maxForce of backleg

#frontleg
am[1] = 1*np.pi/4         #amplitude of front
f[1] = 4*np.pi/iter*10    #frequency of frontleg
p[1] = 0                     #phaseOffset of frontleg
F[1] = 22                    #phaseOffset of backleg

amplitude_FrontLeg= np.pi/4
frequency_FrontLeg=10
phaseOffset_FrontLeg=0

amplitude_BackLeg= np.pi/4
frequency_BackLeg=20
phaseOffset_BackLeg=np.pi/6
targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, 1000))
print('targetAngles: ', targetAngles_BackLeg)

'''




