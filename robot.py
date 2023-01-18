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
		
		#self.world = WORLD(p)
		
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
			#SENSOR
			#Get_Value(time)
			#SENSOR.Get_Value(<#time#>)
			#backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
			#print(backLegTouch)
		
	def Prepare_To_Act(self):
		i=0
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)
			self.motors[jointName].Prepare_To_Act()
			self.motors[jointName].Set_Value(c.am[i],c.p[i],c.f[i],c.F[i])
			#print(c.am[i])
			i=i+1
			
	def Sense(self,t):
		for linkName in pyrosim.linkNamesToIndices:
			#print(linkName)
			self.sensors[linkName].Get_Value(t)
			
	def Act(self,t):
		for jointName in pyrosim.jointNamesToIndices:
			pyrosim.Set_Motor_For_Joint(
			bodyIndex = self.robotId,
			jointName = jointName,
			controlMode = p.POSITION_CONTROL,
			targetPosition = self.motors[jointName].motorValues[t],
			maxForce = self.motors[jointName].force)
			
	def Save_Values(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName].Save_Values()
			
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName].Save_Values()
			
			#self.motors[jointName] = sensor.MOTOR(jointName)
			