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
	def __init__(self, directOrGUI, solutionID):
		
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
			
			self.time_sleep=0
		elif directOrGUI == 'GUI':
			
			self.physicsClient = p.connect(p.GUI)
			self.time_sleep=1/60 #1/1000
		
		
		p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
		
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT(solutionID)
		#p.loadSDF("world.sdf")		
		
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
			time.sleep(self.time_sleep)
			self.robot.Save_Values()#	
	
	def Get_Fitness(self):
		self.robot.Get_Fitness()
		