#!/usr/bin/env python3

#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random
import pandas as pd



iter=10000 #iteration times

numpyseed=80000

randomseed=700
np.random.seed(numpyseed)
random.seed(randomseed)

col=1

fitness_Values=[]





populationSize= 10
numberOfGenerations= 500

x_cordinates= [i for i in range(numberOfGenerations+1)]
df=pd.DataFrame()
df['Generation']=x_cordinates

motorJointRange=0.7

maxLinks=10
#maxLinkSize = 1

color_No_Sensor_Link= 'Blue'
rgba_No_Sensor_Link= '0.0 0.0 1.0 1.0'


#number_of_links= random.randint(5,maxLinks)
#randSensorsList = [random.randint(0,1) for _ in range (number_of_links)]

color_Sensor_Link='Green'


rgba_Sensor_Link='0.0 1.0 0.0 1.0'
numSensorNeurons=10
numMotorNeurons=9


#maxLinks = 10


#childrenPerParent = 10
#
#directionDict = {
#	"up": [0,0,1],
#	"down": [0,0,-1],
#	"right": [0,1,0],
#	"left": [0,-1,0],
#	"backward": [1,0,0],
#	"forward": [-1,0,0]
#}
#directionInverseDict = {
#	"up": "down",
#	"down": "up",
#	"left": "right",
#	"right": "left",
#	"forward": "backward",
#	"backward": "forward"}
#
#
#
#

#------------------------
#FrontLeg 
amplitude_FrontLeg= np.pi/7
frequency_FrontLeg=10
phaseOffset_FrontLeg=0
targetAngles_FrontLeg = np.sin(np.linspace(0, np.pi*2, iter))
maxForce_FrontLeg=40


amplitude_BackLeg= np.pi/7
frequency_BackLeg=19
phaseOffset_BackLeg= np.pi/3
targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, iter))
maxForce_BackLeg=50

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




	