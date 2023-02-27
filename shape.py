#!/usr/bin/env python3

import random
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np


class SHAPE:
	def __init__(self, ID, parent=None, direction="right"):
		self.IDNum = ID
		self.ID = f"Link{ID}"
		self.parent = parent
		self.directionString = direction
		self.linkDirection_Vector = np.array(c.directionDict[direction])
		self.jointDirection_Vector = np.copy(self.linkDirection_Vector)
		if False:
			self.dimensions = [random.uniform(0.25, self.parent.dimensions[0]), 
								random.uniform(0.25, self.parent.dimensions[1]), 
								random.uniform(0.25, self.parent.dimensions[2])]
		else:
			self.dimensions = [random.uniform(0.25, c.maxLinkSize)*0.8, 
								random.uniform(0.25, c.maxLinkSize), 
								random.uniform(0.25, c.maxLinkSize)*0.5]
		self.children = []
		#self.initialize_color()
		
	def create(self, liklihood_of_branching, first_pass=True):
		self.isTurning = self.parent.directionString != self.directionString
		if first_pass:
			self.jointDirectionVector += self.parent.linkDirection_Vector
		self.jointPos = self.parent.dimensions * self.jointDirection_Vector* 0.5
		self.linkPos = self.dimensions * self.linkDirectionVector * 0.5
		self.jointAxis = np.array2string(np.absolute(1-self.linkDirection_Vector))
		
		self.jointID = f"{self.parent.ID}_{self.ID}"
		
		
		pyrosim.Send_Joint(name = self.jointID,
			parent= self.parent.ID , 
			child = self.ID , 
			type = "revolute", 
			position = self.jointPos,
			jointAxis = self.jointAxis)
		pyrosim.Send_Cube(name=f"{self.ID}",
			pos=self.linkPos, 
			size=self.dimensions,
			color=self.linkColorDims,
			colorName = self.linkColorName)
		
		if (random.random() < liklihood_of_branching) and first_pass:
			potential_branch_directions = list(c.directionDict.keys())
			potential_branch_directions.remove(self.directionString)
			potential_branch_directions.remove(c.directionInverseDict[self.directionString])
			branch_direction = random.choice(potential_branch_directions)
			branch_length = random.randint(1,5)
			parent = self
			for i in range(0,branch_length):
				child = LINK(f"{self.IDNum}-{i}", parent, branch_direction)
				child.create(liklihood_of_branching-0.4)
				self.children.append(child)
				parent = child
				
				
				
	def initialize_color(self):
		self.isSensor = random.choice([True, False])
		if self.isSensor:
			self.linkColorDims = "0 1.0 0 1.0"
			self.linkColorName = "Green"
		else:
			self.linkColorDims = "0 0 1.0 1.0"
			self.linkColorName = "Blue"
	def Send_Shape(self, shape, name, pos, size, mass, material_name , rgba):
			print(shape)
			if shape=='sphere':
				radius=[size[1]/2] #initializing the random assigned width as radius length
				print("Sphere :",radius)
				pyrosim.Send_Sphere(name=name , pos= pos, size=radius, mass=mass, material_name=material_name, rgba=rgba)
			elif shape=='cube':
				pyrosim.Send_Cube(name=name , pos= pos, size=size, mass=mass, material_name=material_name, rgba=rgba)
				
				