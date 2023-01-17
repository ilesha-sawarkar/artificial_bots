#!/usr/bin/env python3


import pybullet as p

class WORLD :
	def __init__(self, p ):
		self.planeId = p.loadURDF("plane.urdf")
		#self.robotId = p.loadURDF("body.urdf")
		p.loadSDF("world.sdf")
		