#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random
import os


os.system(f"python3 generate.py ")



physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(1000)
print('backLegSensorValues: ' ,backLegSensorValues)

frontLegSensorValues = np.zeros(1000)
print('frontLegSensorValues: ' ,frontLegSensorValues)

#targetAngles = np.linspace(0, math.pi*2, num=1000)
targetAngles = np.sin(np.linspace(0, np.pi*2, 1000))
#targetAngles= (targetAngles/2)*(np.pi/2)


#FrontLeg 
amplitude_FrontLeg= np.pi/3
frequency_FrontLeg=10
phaseOffset_FrontLeg=0


targetAngles_FrontLeg = np.sin(np.linspace(0, np.pi*2, 1000))
print('targetAngles: ', targetAngles_FrontLeg)


for i in range (0,len(targetAngles_FrontLeg)):
	targetAngles_FrontLeg[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg[i] + phaseOffset_FrontLeg)
print('targetAngles: ', targetAngles_FrontLeg)

#----------------------------------------
#Backleg

amplitude_BackLeg= np.pi/3
frequency_BackLeg=10
phaseOffset_BackLeg=np.pi/4
targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, 1000))
print('targetAngles: ', targetAngles_BackLeg)


for i in range (0,len(targetAngles_BackLeg)):
	targetAngles_BackLeg[i]= amplitude_BackLeg * np.sin(frequency_BackLeg * targetAngles_BackLeg[i] + phaseOffset_BackLeg)
print('targetAngles: ', targetAngles_BackLeg)

#np.save('data/targetAngles_BackLeg.npy', targetAngles_BackLeg) 
#np.save('data/targetAngles_FrontLeg.npy', targetAngles_FrontLeg) 

#exit()
for i in range (0,1000):
	p.stepSimulation()
	
	
	#backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("Torso_Lower_RightLeg")
	#print(backLegTouch)
	#frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("Torso_Lower_LeftLeg")
	time.sleep(1/1200)
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("RightLeg2")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("LeftLeg2")
	
	pyrosim.Set_Motor_For_Joint(robotId,
		jointName = "Lower_LeftLeg2",
		controlMode = p.POSITION_CONTROL,
		targetPosition = targetAngles_BackLeg[i],
		#random.randrange(int(-math.pi/2),int(math.pi/2)),
		maxForce = 20)
	
	pyrosim.Set_Motor_For_Joint(robotId,
		jointName = "Lower_RightLeg2",
		controlMode = p.POSITION_CONTROL,
		targetPosition = targetAngles_FrontLeg[i],
		#random.randrange(int(-math.pi/2),int(math.pi/2)),
		# +math.pi/4.0,
		maxForce = 22)
	
	print('backLegSensorValues: ' ,backLegSensorValues)
	print('frontLegSensorValues: ' ,frontLegSensorValues)


	#np.save('data/backLegSensorValues.npy', backLegSensorValues) 
	#np.save('data/frontLegSensorValues.npy', frontLegSensorValues) 


p.disconnect()