#!/usr/bin/env python3

from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np 
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT :
	def __init__(self):
		self.robotId = p.loadURDF("body.urdf")
		self.motors={}
		self.sensors={}
		self.nn = NEURAL_NETWORK("brain.nndf")

		
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
			
			#print(linkName)

		
	def Prepare_To_Act(self, ):
		i=0
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)
			self.motors[jointName].Prepare_To_Act()
			self.motors[jointName].Set_Value(self.robotId, i)
			#print(c.am[i])
			i=i+1
		
		
	def Act(self,t):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)    
				desiredAngle = self.nn.Get_Value_Of(neuronName)   
				#print(jointName, desiredAngle)
		
				self.motors[jointName].Set_Value(self.robotId, desiredAngle)
				#print(neuronName)
				#for jointName in pyrosim.jointNamesToIndices:
				#self.motors[jointName].Set_Value(self.robotId, t)
	
	def Think(self):
		self.nn.Update()
		#self.nn.Print()
		
		
	def Save_Values(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName].Save_Values()
			
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName].Save_Values()
			
			#self.motors[jointName] = sensor.MOTOR(jointName)
			