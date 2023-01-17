#!/usr/bin/env python3

#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random




backLegSensorValues = np.zeros(1000)
print('backLegSensorValues: ' ,backLegSensorValues)

frontLegSensorValues = np.zeros(1000)
print('frontLegSensorValues: ' ,frontLegSensorValues)


#FrontLeg 
amplitude_FrontLeg= np.pi/4
frequency_FrontLeg=10
phaseOffset_FrontLeg=0


targetAngles_FrontLeg = np.sin(np.linspace(0, np.pi*2, 1000))
print('targetAngles: ', targetAngles_FrontLeg)


for i in range (0,len(targetAngles_FrontLeg)):
	targetAngles_FrontLeg[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg[i] + phaseOffset_FrontLeg)
print('targetAngles: ', targetAngles_FrontLeg)

#----------------------------------------
#Backleg

amplitude_BackLeg= np.pi/4
frequency_BackLeg=20
phaseOffset_BackLeg=np.pi/6
targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, 1000))
print('targetAngles: ', targetAngles_BackLeg)


for i in range (0,len(targetAngles_BackLeg)):
	targetAngles_BackLeg[i]= amplitude_BackLeg * np.sin(frequency_BackLeg * targetAngles_BackLeg[i] + phaseOffset_BackLeg)
print('targetAngles: ', targetAngles_BackLeg)

#np.save('data/targetAngles_BackLeg.npy', targetAngles_BackLeg) 
#np.save('data/targetAngles_FrontLeg.npy', targetAngles_FrontLeg) 

