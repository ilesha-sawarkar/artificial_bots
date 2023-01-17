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


simulation = SIMULATION()	

'''
print('backLegSensorValues: ' ,c.backLegSensorValues)

print('frontLegSensorValues: ' ,c.frontLegSensorValues)




print('targetAngles Front: ', c.targetAngles_FrontLeg)

print('targetAngles Back: ', c.targetAngles_BackLeg)


for i in range (0,1000):
	p.stepSimulation()
	
	
	backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	print(backLegTouch)
	frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	time.sleep(1/20)
	c.backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	c.frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	
	pyrosim.Set_Motor_For_Joint(robotId,
	jointName = "Torso_BackLeg",
	controlMode = p.POSITION_CONTROL,
	targetPosition = c.targetAngles_BackLeg[i],
	#random.randrange(int(-math.pi/2),int(math.pi/2)),
	maxForce = 50)
	
	pyrosim.Set_Motor_For_Joint(robotId,
	jointName = "Torso_FrontLeg",
	controlMode = p.POSITION_CONTROL,
	targetPosition = c.targetAngles_FrontLeg[i],
	#random.randrange(int(-math.pi/2),int(math.pi/2)),
	# +math.pi/4.0,
	maxForce = 50)
	
print('backLegSensorValues: ' ,c.backLegSensorValues)
print('frontLegSensorValues: ' ,c.frontLegSensorValues)


np.save('data/backLegSensorValues.npy', c.backLegSensorValues) 
np.save('data/frontLegSensorValues.npy', c.frontLegSensorValues) 

'''
