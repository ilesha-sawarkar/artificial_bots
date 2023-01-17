#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim

from world import WORLD
from robot import ROBOT

class SIMULATION :
	def __init__(self):
		
		
		physicsClient = p.connect(p.GUI)
		
		
		
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		
		p.setGravity(0,0,-9.8)
		self.world = WORLD(p)
		self.robot = ROBOT()
		#p.loadSDF("world.sdf")		
		pyrosim.Prepare_To_Simulate(self.robotId)
		
		p.disconnect()