#!/usr/bin/env python3
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data


class MOTOR :
	def __init__(self, jointName):
		self.jointName=jointName
		#self.values = np.zeros(1000)
		self.motorValues = np.zeros(c.iter)
		self.Prepare_To_Act()
		
	def Prepare_To_Act(self):
		self.amplitude= c.amplitude_BackLeg
		
		if self.jointName == "Torso_FrontLeg":
			self.frequency= c.frequency_BackLeg/2
		else:
			self.frequency= c.frequency_BackLeg
		self.offset=c.phaseOffset_BackLeg
		
		for i in range (c.iter):
			self.motorValues[i] = self.amplitude * np.sin(self.frequency * i + self.offset)		
		
		
	def Set_Value(self, robotId, desiredAngle):
		pyrosim.Set_Motor_For_Joint(
		bodyIndex = robotId,
		jointName = self.jointName,
		controlMode = p.POSITION_CONTROL,
		targetPosition = desiredAngle,
		maxForce = c.maxForce_BackLeg)
			
	def Save_Values(self):
		np.save('motor_value_'+self.jointName,self.motorValues)