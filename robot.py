#!/usr/bin/env python3

from sensor import SENSOR
from motor import MOTOR


class ROBOT :
	def __init__(self):
		robot = ROBOT()	
		self.sensors={}
		self.motors={}