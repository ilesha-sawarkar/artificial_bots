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
import os

class ROBOT :
	def __init__(self,solutionID, objects):
		self.robotId = p.loadURDF(f"body/body{solutionID}.urdf") #, flags=p.URDF_USE_SELF_COLLISION_EXCLUDE_PARENT)
		self.motors={}
		self.sensors={}
		
		self.nn = NEURAL_NETWORK(f"brain/brain{solutionID}.nndf")
		
		self.solutionID=solutionID
		self.world_objects=objects
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_To_Act()
		
		os.system(f"rm brain/brain{self.solutionID}.nndf")
		os.system(f"rm body/body{self.solutionID}.urdf")
		

		
	def Prepare_To_Sense(self):
		for linkName in pyrosim.linkNamesToIndices:
			#print(self.sensors)
			self.sensors[linkName] = SENSOR(linkName)

		
	def Sense(self, time):
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName].Get_Value(time)
			
			#print(linkName)

		
	def Prepare_To_Act(self):
		
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)

			#i=i+1
		
		
	def Act(self,t):
		#print('Here')
		for neuronName in self.nn.Get_Neuron_Names():
			
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)    
				desiredAngle = self.nn.Get_Value_Of(neuronName)*c.motorJointRange   
				self.motors[jointName].Set_Value(self.robotId, desiredAngle)
				
				
	
	def Think(self):
		self.nn.Update()
		#self.nn.Print()
		
		
	def Save_Values(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName].Save_Values()
			
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName].Save_Values()
			
			#self.motors[jointName] = sensor.MOTOR(jointName)
	
	def Get_Fitness(self, objects):
		basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
		basePosition = basePositionAndOrientation[0]
		xPositionRobot = basePosition[0]
		yPositionRobot = basePosition[1]
		zPositionRobot = basePosition[2]
		posAndOrientation = p.getBasePositionAndOrientation(self.world_objects[0])
		position= posAndOrientation[0]
		xPosition_Target = position[0]
		yPosition_Target  = position[1]
		height_Target  = position[2]
		distance = np.sqrt((xPosition_Target-xPositionRobot)**2 + (yPosition_Target-yPositionRobot)**2)
		fitness_file = open(f"data/tmp{self.solutionID}.txt", "w")
		fitness_file.write(str(distance))
		
		os.system(f"mv data/tmp{self.solutionID}.txt data/fitness{self.solutionID}.txt")
		fitness_file.close()
				