#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
from world import WORLD
from robot import ROBOT
import time


class SIMULATION :
	def __init__(self, directOrGUI):
		
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
		elif directOrGUI == "GUI":
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
		
	
	def Run(self ):
		for i in range (0,c.iter):
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Think()
			self.robot.Act(i)
			# step time
			time.sleep(1/10)
			self.robot.Save_Values()#	
	
	def Get_Fitness(self):
		self.robot.Get_Fitness()
		