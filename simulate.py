#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import os


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(100)
print('backLegSensorValues: ' ,backLegSensorValues)

frontLegSensorValues = np.zeros(100)
print('frontLegSensorValues: ' ,frontLegSensorValues)


for i in range (0,100):
	p.stepSimulation()
	
	
	backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	print(backLegTouch)
	frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	time.sleep(1/60)
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	
print('backLegSensorValues: ' ,backLegSensorValues)
print('frontLegSensorValues: ' ,frontLegSensorValues)


np.save('data/backLegSensorValues.npy', backLegSensorValues) 
np.save('data/frontLegSensorValues.npy', frontLegSensorValues) 


p.disconnect()