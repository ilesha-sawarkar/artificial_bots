#!/usr/bin/env python3
import numpy as np
import constants as c

class MOTOR :
	def __init__(self, jointName):
		self.jointName=jointName
		#self.values = np.zeros(1000)
		self.Prepare_To_Act()
		
	def Prepare_To_Act(self):
		self.amplitude = 0
		self.phaseOffset = 0
		self.frequency = 0
		self.force = 0
		self.motorValues = np.zeros(c.iter)
		
	def Set_Value(self,a,p,f,F):
		self.amplitude = a
		self.phaseOffset = p
		self.frequency = f
		self.force = F
		for i in range (c.iter):
			self.motorValues[i] = self.amplitude * np.sin(self.frequency * i + self.phaseOffset)
			
	def Save_Values(self):
		np.save('motor_value_b'+str(self.jointName),self.motorValues)