#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim

from world import WORLD
from robot import ROBOT
import time

class SIMULATION :
	def __init__(self):
		
		
		self.physicsClient = p.connect(p.GUI)
		
		
		
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT()
		#p.loadSDF("world.sdf")		
		pyrosim.Prepare_To_Simulate(self.robot.robotId)
		self.robot.Prepare_To_Sense()
		self.robot.Prepare_To_Act()
		#Run()
		
	def __del__(self):
		p.disconnect()
		
	
	def Run(self, ):
		for i in range (0,1000):
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Act(i)
			# step time
			time.sleep(0.01)
			self.robot.Save_Values()#			
#			backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#			frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
#		
#			pyrosim.Set_Motor_For_Joint(robotId,
#			jointName = "Torso_BackLeg",
#			controlMode = p.POSITION_CONTROL,
#			targetPosition = targetAngles_BackLeg[i],
#			#random.randrange(int(-math.pi/2),int(math.pi/2)),
#			maxForce = 20)
#		
#			pyrosim.Set_Motor_For_Joint(robotId,
#			jointName = "Torso_FrontLeg",
#			controlMode = p.POSITION_CONTROL,
#			targetPosition = targetAngles_FrontLeg[i],
#			#random.randrange(int(-math.pi/2),int(math.pi/2)),
#			# +math.pi/4.0,
#			maxForce = 22)
#		
#			print('backLegSensorValues: ' ,backLegSensorValues)
#			print('frontLegSensorValues: ' ,frontLegSensorValues)
			
			