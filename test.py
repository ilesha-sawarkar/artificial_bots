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

#backLegSensorValues = np.zeros(1000)
#backLegSensorValues_2 = np.zeros(1000)
#print('backLegSensorValues: ' ,backLegSensorValues)

frontLegSensorValues_L = np.zeros(1000)
Lower_frontLegSensorValues_L = np.zeros(1000)
frontLegSensorValues_R = np.zeros(1000)
Lower_frontLegSensorValues_R = np.zeros(1000)
#print('frontLegSensorValues: ' ,frontLegSensorValues)

#targetAngles = np.linspace(0, math.pi*2, num=1000)
targetAngles = np.sin(np.linspace(0, np.pi*2, 1000))
#targetAngles= (targetAngles/2)*(np.pi/2)


#FrontLeg 
amplitude_FrontLeg= np.pi/3
frequency_FrontLeg=10
phaseOffset_FrontLeg=0


targetAngles_FrontLeg_L = np.sin(np.linspace(0, np.pi*2, 1000))
targetAngles_Lower_FrontLeg_L = np.sin(np.linspace(0, np.pi*2, 1000))
targetAngles_FrontLeg_R = np.sin(np.linspace(0, np.pi*2, 1000))
targetAngles_Lower_FrontLeg_R = np.sin(np.linspace(0, np.pi*2, 1000))
#print('targetAngles: ', targetAngles_FrontLeg)


for i in range (0,len(targetAngles_FrontLeg_L)):
	targetAngles_FrontLeg_L[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg_L[i] + phaseOffset_FrontLeg)
for i in range (0,len(targetAngles_Lower_FrontLeg_L)):
	targetAngles_Lower_FrontLeg_L[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_Lower_FrontLeg_L[i] + phaseOffset_FrontLeg)
for i in range (0,len(targetAngles_FrontLeg_R)):
	targetAngles_FrontLeg_R[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg_R[i] + phaseOffset_FrontLeg)
for i in range (0,len(targetAngles_Lower_FrontLeg_R)):
	targetAngles_Lower_FrontLeg_R[i]= amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_Lower_FrontLeg_R[i] + phaseOffset_FrontLeg)	

	#print('targetAngles: ', targetAngles_FrontLeg)

#----------------------------------------
#Backleg

amplitude_BackLeg= np.pi/3
frequency_BackLeg=10
phaseOffset_BackLeg=np.pi/4
#targetAngles_BackLeg = np.sin(np.linspace(0, np.pi*2, 1000))
#targetAngles_BackLeg_2 = np.sin(np.linspace(0, np.pi*2, 1000))
#
#print('targetAngles: ', targetAngles_BackLeg)
#
#
#for i in range (0,len(targetAngles_BackLeg)):
#	targetAngles_BackLeg[i]= amplitude_BackLeg * np.sin(frequency_BackLeg * targetAngles_BackLeg[i] + phaseOffset_BackLeg)
#	
#for i in range (0,len(targetAngles_BackLeg_2)):
#	targetAngles_BackLeg_2[i]= amplitude_BackLeg * np.sin(frequency_BackLeg * targetAngles_BackLeg[i] + phaseOffset_BackLeg)
	

#np.save('data/targetAngles_BackLeg.npy', targetAngles_BackLeg) 
#np.save('data/targetAngles_FrontLeg.npy', targetAngles_FrontLeg) 

#exit()
for i in range (0,1000):
	p.stepSimulation()
	
#	
#	frontLeg_L = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeftLeg")
#	Lower_frontLeg_L = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLowerRightLeg")
#	#print(Lower_frontLeg_L)
#	frontLeg_R = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontRightLeg")
	#Lower_frontLeg_R = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_FrontRightLeg")
	
#	backLeg = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_BackLeftLeg2")
#	backLeg2 = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_BackRightLeg2")
	#print(backLegTouch)
	#frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("Torso_Lower_LeftLeg")
	time.sleep(1/1200)
	#backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_FrontLeftLeg2")
	#backLegSensorValues_2[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_FrontRightLeg2")
	
	##frontLegSensorValues_L[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeftLeg")
	#Lower_frontLegSensorValues_L[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_FrontLeftLeg2")
	##frontLegSensorValues_R[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontRightLeg")
	#Lower_frontLegSensorValues_R[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Lower_FrontRightLeg2")
	
#	pyrosim.Set_Motor_For_Joint(robotId,
#		jointName = "Torso_FrontLeftLeg",
#		controlMode = p.POSITION_CONTROL,
#		targetPosition = targetAngles_FrontLeg_L[i],
#		#random.randrange(int(-math.pi/2),int(math.pi/2)),
#		maxForce = 20)
#
#\
#	
#	pyrosim.Set_Motor_For_Joint(robotId,
#		jointName = "Torso_FrontRightLeg",
#		controlMode = p.POSITION_CONTROL,
#		targetPosition = targetAngles_FrontLeg_R[i],
#		#random.randrange(int(-math.pi/2),int(math.pi/2)),
#		# +math.pi/4.0,
#		maxForce = 22)
	

#	
#	print('backLegSensorValues: ' ,backLegSensorValues)
#	print('frontLegSensorValues: ' ,frontLegSensorValues)


	#np.save('data/backLegSensorValues.npy', backLegSensorValues) 
	#np.save('data/frontLegSensorValues.npy', frontLegSensorValues) 


p.disconnect()