#!/usr/bin/env python3

from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np 
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim

class ROBOT :
	def __init__(self):
		self.robotId = p.loadURDF("body.urdf")
		self.motors={}
		self.sensors={}

		
	def Prepare_To_Sense(self):
		#self.sensors=SENSOR()
		for linkName in pyrosim.linkNamesToIndices:
			#print(self.sensors)
			self.sensors[linkName] = SENSOR(linkName)
			#print(linkName)
			#print(self.sensors)
		
	def Sense(self, time):
		for linkName in pyrosim.linkNamesToIndices:
			#print(self.sensors)
			self.sensors[linkName].Get_Value(time)
			
		print(linkName)

		
	def Prepare_To_Act(self, ):
		i=0
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)
			self.motors[jointName].Prepare_To_Act()
			self.motors[jointName].Set_Value(self.robotId, i)
			#print(c.am[i])
			i=i+1
		
		
	def Act(self,t):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName].Set_Value(self.robotId, t)
			
			
	def Save_Values(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName].Save_Values()
			
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName].Save_Values()
			
			#self.motors[jointName] = sensor.MOTOR(jointName)
			