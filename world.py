#!/usr/bin/env python3


import pybullet as p

class WORLD :
	def __init__(self ):
		self.planeId = p.loadURDF("plane.urdf")
		#
		self.objects=p.loadSDF("world.sdf")
		