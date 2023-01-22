#!/usr/bin/env python3
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR :
	def __init__(self, linkName):
		#sensor = SENSOR(linkName)	
		self.linkName=linkName
		self.values = np.zeros(1000)


	def Get_Value(self, time):
		self.values[time] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
		#print(self.values[time])
	
	def Save_Values(self):
		np.save('sensordata_'+str(self.linkName),self.values)
			