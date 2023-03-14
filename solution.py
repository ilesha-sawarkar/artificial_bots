#!/usr/bin/env python3

#!/usr/bin/env python3

import os
import pyrosim.pyrosim as pyrosim
import numpy
import random
import time
import constants as c
import math
from collections import Counter
numpy.random.seed(c.numpyseed)
random.seed(c.randomseed)



class SOLUTION:
	def __init__(self, ID):
		numpy.random.seed(c.numpyseed)
		random.seed(c.randomseed)
		print('SEED', c.numpyseed)
		print('Seeed', c.randomseed)
		
		self.weights = numpy.random.rand(c.maxLinks+2,c.maxLinks+2) * 2 - 1
		self.myID = ID
		self.motorNeuronList=[]
		
		self.numSensorNeurons=0
		self.numMotorNeurons=0
		self.motorNeuronList=[]
		self.shapeInfo = []
		self.total_creature_connections = {}
		self.sensorNeuronList =[]
		self.shapesAdded = []
		self.locationMatrix = numpy.zeros((40,40,40))
		self.connections = []
		
		
		
		
		
	def Set_ID(self):
		self.myID += 1
		
	def Start_Simulation(self, directOrGui, child_true=0):
		if (self.myID == 0):
			self.Create_World()
		if (child_true == 1):
			self.Create_Child_Body()
			self.Create_Child_Brain()
		else:
			self.Create_Body()
			self.Create_Brain()
			
		os.system("python3 simulate.py " + str(directOrGui) + " " + str(self.myID) + " & ")  #2>1
		
	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("fitness"+str(self.myID)+".txt"):
			time.sleep(0.01)
		fit_file = open("fitness"+str(self.myID)+".txt", "r")
		fitness = fit_file.read()
		if fitness == '':
			
			time.sleep(0.1)
			fitness = fit_file.read()
		self.fitness = float(fitness)
		print('Fitness: ', self.fitness)
		fit_file.close()
		os.system("rm fitness"+str(self.myID)+".txt")
		return(self.fitness)
	
	
	
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		length = 1
		width = 1
		height = 1
		x = -30
		y = 10
		z = 0.5
		pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
		pyrosim.End()
	
	def Send_Shape(self, shape, name, pos, size, mass, material_name , rgba):
		print(shape)
		if shape=='sphere':
			radius=[size[1]/2] #initializing the random assigned width as radius length
			print("Sphere :",radius)
			pyrosim.Send_Sphere(name=name , pos= pos, size=radius, mass=mass, material_name=material_name, rgba=rgba)
		elif shape=='cube':
			pyrosim.Send_Cube(name=name , pos= pos, size=size, mass=mass, material_name=material_name, rgba=rgba)
			
			
			
	def initialize_shape_and_dimensions(self):
		length = random.randint(1,2) 
		width = random.randint(1,2) 
		height = random.randint(1,2) 
		#shapes=['sphere', 'cube']
		
		shape_choice=random.choice([ 'cube','sphere']) #shape chosen for each link
		
		if shape_choice=='sphere':
			length=int(width)
			height=int(width)
			width=width
			print('Here', shape_choice)
			
		return length, width, height, shape_choice
	
		
	def Create_Child_Body(self):
		pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
		
		color_name = "Cyan"
		
		
		shapeInfo = self.shapeInfo
		total_creature_connections =  self.total_creature_connections
		
		
		sensorNeuronList = self.sensorNeuronList
		shapesAdded = self.shapesAdded
		LinkJoitLink = total_creature_connections.keys()
		
		counter = 0
		
		for link in shapesAdded:
			
			length = shapeInfo[link][0]
			width = shapeInfo[link][1]
			height = shapeInfo[link][2]
			shape_choice= shapeInfo[link][6]
			
			if self.sensorNeuronList[counter]==0: #No Sensor
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
				
			if (link == "Link0"):
				self.Send_Shape(shape_choice, name = link, pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				
				counter += 1
			else:
				for j in LinkJoitLink:
					if ("_" + link) in j:
						jointPositionAxis = total_creature_connections[j]
						linkToJoin = j[0:j.find("_")]
						break
					
				for k in LinkJoitLink:
					if ("_" + linkToJoin) in k:
						grandParAxis = total_creature_connections[k]
						
						
				if (linkToJoin == "Link0"):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0], shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1], shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
					elif (jointPositionAxis == 2):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
					elif (jointPositionAxis == 3):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
					elif (jointPositionAxis == 4):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
					else:                        
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
					self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)	

				elif(grandParAxis == jointPositionAxis):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0],0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [0,shapeInfo[linkToJoin][1],0], jointAxis = "0 1 0")
					elif (jointPositionAxis == 2):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0,0,shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
					elif (jointPositionAxis == 3):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]),0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 4):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [0,-(shapeInfo[linkToJoin][1]),0], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0,0,-(shapeInfo[linkToJoin][2])], jointAxis = "0 0 1")
					self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)		
						
						
				else:
					if (grandParAxis == 0):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)			
					elif (grandParAxis == 1):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), shapeInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)			
							
					elif (grandParAxis == 2):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0,  shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						elif (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0,  shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)	
					# Negative Grand Axises
					elif (grandParAxis == 3):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)	
					elif (grandParAxis == 4):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)	
					else:
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0,  -(shapeInfo[linkToJoin][2]/2)], jointAxis = "1 0 0")
						elif (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 1 0")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link, parent = linkToJoin , child = link , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0,  -(shapeInfo[linkToJoin][2]/2)], jointAxis = "1 0 0")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 1 0")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + link)	
							
				if (jointPositionAxis == 0):
					
					self.Send_Shape(shape_choice, name = link, pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				elif (jointPositionAxis == 1):
					
					self.Send_Shape(shape_choice, name = link, pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPositionAxis == 2):
					
					self.Send_Shape(shape_choice, name = link, pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				# Negative Axis Links
				elif (jointPositionAxis == 3):
					
					self.Send_Shape(shape_choice, name = link, pos=[-length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPositionAxis == 4):
					
					self.Send_Shape(shape_choice, name = link, pos=[0,-width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				else:
					self.Send_Shape(shape_choice, name = link, pos=[0,0,-(height/2)], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
					
				counter += 1
				# flag2 = 1
				
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		self.sensorNeuronList = sensorNeuronList
		self.shapesAdded = shapesAdded
		pyrosim.End()
		
		
		
	def Create_Body(self):
		pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
		# pyrosim.Start_URDF("body.urdf")
		
		
		
		shapeInfo = {}
		shapesAdded = []
		connections = []
		total_creature_connections = {}
		self.LinkJointLink = []
		locationMatrix = self.locationMatrix.copy()
		self.sensorNeuronList
		self.numLinks= random.randint(3,c.maxLinks)
		print('numberofLinks', self.numLinks)
		self.sensorNeuronList= [random.randint(0,1) for _ in range (self.numLinks)]
		print(self.sensorNeuronList)
		minX = 0
		minY = 0
		minZ = 0
		
		maxX = 0
		maxY = 0
		maxZ = 0
		
		
		for i in range(0,self.numLinks):
			# length = random.randint(1,2) * numpy.random.rand()
			# width = random.randint(1,2) * numpy.random.rand()
			# height = random.randint(1,2) * numpy.random.rand()
			
			if self.sensorNeuronList[i]==0: #No Sensor
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
				
			length, width, height, shape_choice = self.initialize_shape_and_dimensions()
			
			
			
			
			if (i == 0):
				self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				
				minX = 20
				minY = 20
				minZ = 0
				for x in range(length):
					for y in range(width):
						for z in range(height):
							locationMatrix[20+x,20+y,0+z] = 1
							maxX = 20+x+1
							maxY = 20+y+1
							maxZ = 0+z+1
			else:
				pass
				
			if(i == 0):
				shapeInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ], shape_choice]
				shapesAdded.append("Link" + str(i))
				result = numpy.where(numpy.logical_and(locationMatrix>0, locationMatrix<2))
				
				
				flag2 = 1
				
			else:
				while(flag2 == 1):
					jointPositionAxis = random.choice([0, 1, 2, 3, 4, 5])
					linkToJoin = random.choice(shapesAdded)
					
					if ([jointPositionAxis,linkToJoin] in connections):
						pass
					else:
						linkToJoinPointX = shapeInfo[linkToJoin][3]
						linkToJoinPointY = shapeInfo[linkToJoin][4]
						linkToJoinPointZ = shapeInfo[linkToJoin][5]
						
						MidPointX = (linkToJoinPointX[0]+linkToJoinPointX[1])/2
						MidPointY = (linkToJoinPointY[0]+linkToJoinPointY[1])/2
						MidPointZ = (linkToJoinPointZ[0]+linkToJoinPointZ[1])/2
						
						tempLocationMatrix = locationMatrix.copy()
						
						inner_flag1 = 0
						inner_flag2 = 0
						
						if jointPositionAxis == 0:
							minX = linkToJoinPointX[1]
							maxX = minX + length
							minY = MidPointY - width/2
							maxY = minY + width
							minZ = MidPointZ - height/2
							maxZ = minZ + height
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions() 
								inner_flag1 = 1
								
							for x2 in range(math.ceil(maxX) - math.floor(minX)):
								for y2 in range(math.ceil(maxY) - math.floor(minY)):
									for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											
											if (locationMatrix[math.floor(x2 + linkToJoinPointX[1]), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] == 1):           
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												break
											else:
												flag2 = 0
												
												tempLocationMatrix[math.floor(x2 + linkToJoinPointX[1]), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] = 1
												
												
												
												
										# if (locationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
										elif (locationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == 1):           
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											
											tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
											
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
						elif jointPositionAxis == 1:
							minX = MidPointX - length/2
							maxX = minX + length
							minY = linkToJoinPointY[1]
							maxY = minY + width
							minZ = MidPointZ - height/2
							maxZ = minZ + height
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions()
								
								inner_flag1 = 1
								
							for x2 in range(math.ceil(maxX) - math.floor(minX)):
								for y2 in range(math.ceil(maxY) - math.floor(minY)):
									for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											
											if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(y2 + linkToJoinPointY[1]), math.floor(MidPointZ - height/2 + z2)] == 1):
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												break
											
											else:
												flag2 = 0
												
												tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(y2 + linkToJoinPointY[1]), math.floor(MidPointZ - height/2 + z2)] = 1
												
												
										# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
										elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == 1):
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											
											tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] = 1
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
						elif jointPositionAxis == 2:
							minX = MidPointX - length/2
							maxX = minX + length
							minY = MidPointY - width/2
							maxY = minY + width
							minZ = linkToJoinPointZ[1]
							maxZ = minZ + height
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions()
								inner_flag1 = 1
								
							for x2 in range(math.ceil(maxX) - math.floor(minX)):
								for y2 in range(math.ceil(maxY) - math.floor(minY)):
									for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(z2 + linkToJoinPointZ[1])] == 1):                                            
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												break
											
											else:
												flag2 = 0
												
												tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(z2 + linkToJoinPointZ[1])] = 1
												
												
										# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
										elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == 1):                                            
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										else:
											flag2 = 0
											
											tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] = 1
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
						# Negative Axis
						elif jointPositionAxis == 3:
							
							maxX = linkToJoinPointX[0]
							minX = maxX - length
							minY = MidPointY - width/2
							maxY = minY + width
							minZ = MidPointZ - height/2
							maxZ = minZ + height
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions()
								inner_flag1 = 1
								
							for x2 in range(1,math.floor(maxX) - math.floor(minX)+1):
								for y2 in range(math.ceil(maxY) - math.floor(minY)):
									for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											
											if (locationMatrix[math.floor(linkToJoinPointX[0] - x2), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] == 1):           
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												
												
												break
											else:
												flag2 = 0
												tempLocationMatrix[math.floor(linkToJoinPointX[0] - x2), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] = 1
												
												
										elif (locationMatrix[math.floor(linkToJoinPointX[0] - x2), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == 1):           
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											tempLocationMatrix[math.floor(linkToJoinPointX[0] - x2), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
						elif jointPositionAxis == 4:
							minX = MidPointX - length/2
							maxX = minX + length
							maxY = linkToJoinPointY[0]
							minY = maxY - width
							minZ = MidPointZ - height/2
							maxZ = minZ + height
							
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions()
								inner_flag1 = 1
								
							for x2 in range(math.ceil(maxX) - math.floor(minX)):
								for y2 in range(1,math.floor(maxY) - math.floor(minY)+1):
									for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											
											if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.floor(MidPointZ - height/2 + z2)] == 1):
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												break
											
											else:
												flag2 = 0
												tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.floor(MidPointZ - height/2 + z2)] = 1
												
												
										elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.ceil(MidPointZ - height/2 + z2)] == 1):
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.ceil(MidPointZ - height/2 + z2)] = 1
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
						else:
							minX = MidPointX - length/2
							maxX = minX + length
							minY = MidPointY - width/2
							maxY = minY + width
							maxZ = linkToJoinPointZ[0]
							minZ = maxZ - height
							if (minX < 0) or (minY < 0) or (minZ < 0):
								flag2 = 1
								tempLocationMatrix = locationMatrix.copy()
								length, width, height, shape_choice = self.initialize_shape_and_dimensions()
								inner_flag1 = 1
								
							for x2 in range(math.ceil(maxX) - math.floor(minX)):
								for y2 in range(math.ceil(maxY) - math.floor(minY)):
									for z2 in range(1,math.floor(maxZ) - math.floor(minZ)+1):
										
										if (x2 == 0) or (y2 == 0) or (z2 == 0):
											if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] == 1):                                            
												flag2 = 1
												tempLocationMatrix = locationMatrix.copy()
												inner_flag1 = 1
												break
											
											else:
												flag2 = 0
												
												tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] = 1
												
												
										# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
										elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] == 1):                                            
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										else:
											flag2 = 0
											
											tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] = 1
										if inner_flag1 == 1:
											inner_flag2 = 1
											flag2 = 1
											break
									if inner_flag2 == 1:
											break
									
									
				locationMatrix = tempLocationMatrix.copy()
				result = numpy.where(numpy.logical_and(locationMatrix>0, locationMatrix<2))
				
				
				shapeInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ], shape_choice]
				
				shapesAdded.append("Link" + str(i))
				connections.append([jointPositionAxis,linkToJoin])  
				total_creature_connections[linkToJoin+"_"+"Link"+ str(i)] = jointPositionAxis
				self.connections = connections
				
				for li in reversed(range(len(self.LinkJointLink))) :
					if ("_"+linkToJoin) in self.LinkJointLink[li]:
						grandparentLink = self.LinkJointLink[li]
						grandParAxis = total_creature_connections[grandparentLink]
						break
					
					
				if (linkToJoin == "Link0"):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0], shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1], shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
					elif (jointPositionAxis == 2):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
					elif (jointPositionAxis == 3):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
					elif (jointPositionAxis == 4):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
					self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))	
						
						
				elif(grandParAxis == jointPositionAxis):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0],0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [0,shapeInfo[linkToJoin][1],0], jointAxis = "0 1 0")
					elif (jointPositionAxis == 2):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0,0,shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
					elif (jointPositionAxis == 3):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]),0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 4):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [0,-(shapeInfo[linkToJoin][1]),0], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0,0,-(shapeInfo[linkToJoin][2])], jointAxis = "0 0 1")
					self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))	
						
						
				else:
					if (grandParAxis == 0):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))	
					elif (grandParAxis == 1):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), shapeInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))
							
							
					elif (grandParAxis == 2):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0,  shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						elif (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0,  shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))
						
					# Negative Grand Axises
					elif (grandParAxis == 3):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "0 1 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))
						
							
					elif (grandParAxis == 4):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 2):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), -(shapeInfo[linkToJoin][1]/2), 0], jointAxis = "1 0 0")
						elif (jointPositionAxis == 5):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 0 1")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))
						
							
					else:
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0,  -(shapeInfo[linkToJoin][2]/2)], jointAxis = "1 0 0")
						elif (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 1 0")
						elif (jointPositionAxis == 3):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [-(shapeInfo[linkToJoin][0]/2), 0,  -(shapeInfo[linkToJoin][2]/2)], jointAxis = "1 0 0")
						elif (jointPositionAxis == 4):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, -(shapeInfo[linkToJoin][1]/2), -(shapeInfo[linkToJoin][2]/2)], jointAxis = "0 1 0")
						self.motorNeuronList.append(linkToJoin + "_" + "Link" + str(i))
						
							
							
				if (jointPositionAxis == 0):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				elif (jointPositionAxis == 1):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				elif (jointPositionAxis == 2):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				# Negative Axis Links
				elif (jointPositionAxis == 3):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[-length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPositionAxis == 4):
					
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,-width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				else:
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,0,-height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				self.LinkJointLink.append(linkToJoin + "_" + "Link" + str(i))
				
				flag2 = 1
				
		self.locationMatrix = locationMatrix.copy()
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		#self.sensorNeuronList = c.sensorNeuronList
		self.shapesAdded = shapesAdded
		
		pyrosim.End()
		
	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain/brain"+str(self.myID)+".nndf")
		print('listbrain', self.sensorNeuronList)
		self.numSensorNeurons=self.sensorNeuronList.count(1)
		self.numMotorNeurons = len(self.motorNeuronList)
		#self.weights = (np.random.rand(self.numSensorNeurons,self.numMotorNeurons)) * 2 - 1
		print('Sensors: ',self.numSensorNeurons,'Motors: ',self.numMotorNeurons)
		print("synapse_weights: ", self.weights)
		
		i=0
		for link in self.sensorNeuronList:
			if link==1:
				pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link"+str(i))
				i+=1
				
		print(self.motorNeuronList)
		for joint in self.motorNeuronList:
				pyrosim.Send_Motor_Neuron( name = i , jointName = joint)
				i+=1
			
			
		for currentRow in range(0,self.numSensorNeurons):
			for currentColumn in range(0, self.numMotorNeurons):
				
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+ self.numSensorNeurons , 
					weight = self.weights[currentRow][currentColumn] )	
				
		pyrosim.End()
		
	def Create_Child_Brain(self):
			pyrosim.Start_NeuralNetwork("brain/brain"+str(self.myID)+".nndf")
			
			counter = 0
			#numSensorNeurons=self.sensorNeurons.count(1)
			numLinks = len(self.shapesAdded)
			for i in range(0,numLinks):
				if (self.sensorNeuronList[i] == 1):
					pyrosim.Send_Sensor_Neuron(name = counter , linkName = self.shapesAdded[i])
					counter += 1
					
			child_LinkJointLink = self.total_creature_connections.keys()
			listLJL = list(child_LinkJointLink)
			self.numSensorNeurons=self.sensorNeuronList.count(1)
			for j in range(0,numLinks - 1):
				pyrosim.Send_Motor_Neuron( name = j + self.numSensorNeurons  , jointName = listLJL[j])
				
			for currentRow in range(0,self.numSensorNeurons):
				for currentColumn in range(0, self.numMotorNeurons):
					
					pyrosim.Send_Synapse( 
						sourceNeuronName = currentRow , 
						targetNeuronName = currentColumn+ self.numSensorNeurons , 
						weight = self.weights[currentRow][currentColumn] )						
			pyrosim.End()
		
		
	def Mutate(self):
		shapeInfo = self.shapeInfo
		total_creature_connections =  self.total_creature_connections
		sensorNeuronList = self.sensorNeuronList
		shapesAdded = self.shapesAdded
		LinkJoitLink = total_creature_connections.keys()
		LinkJoiNtLink = list(LinkJoitLink)
		locationMatrix = self.locationMatrix.copy()
		connections = self.connections
		
		# 0 - Remove Link/ 1 - Add Link/ 2 - None
		add_remove_none = 2
		if len(LinkJoiNtLink) > 3 and len(LinkJoiNtLink) < c.maxLinks:
			add_remove_none = random.choice([0, 1, 2])
			# add_remove_none = 0
		elif len(LinkJoiNtLink) > 3 and len(LinkJoiNtLink) >= c.maxLinks:
			add_remove_none = random.choice([0, 2])
		elif len(LinkJoiNtLink) < 3:
			add_remove_none = random.choice([1, 2])
			
			
			
		# Remove Link
			
		if (add_remove_none == 0):
			LinksWithChild = []
			for li in shapesAdded:
				for j in LinkJoiNtLink:
						if (li + "_" ) in j:
							LinksWithChild.append(li)
			childlessLinks = list((Counter(shapesAdded)-Counter(LinksWithChild)).elements())
			linkToRemove = random.choice(childlessLinks)
			shapesAdded.remove(linkToRemove)
			del shapeInfo[linkToRemove]
			sensorNeuronList.pop()
			
			for lj in LinkJoiNtLink:
				if("_" + linkToRemove) in lj:
					LinkJoitLinkToRemove = lj
					break
				
				
			del total_creature_connections[LinkJoitLinkToRemove]
			
			
			
			
		elif(add_remove_none == 1):
			length, width, height, shape_choice = self.initialize_shape_and_dimensions()
			
			flag2 = 1
			while(flag2 == 1):
				jointPositionAxis = random.choice([0, 1, 2, 3, 4, 5])
				
				linkToJoin = random.choice(shapesAdded)
				
				if ([jointPositionAxis,linkToJoin] in connections):
					pass
				else:
					linkToJoinPointX = shapeInfo[linkToJoin][3]
					linkToJoinPointY = shapeInfo[linkToJoin][4]
					linkToJoinPointZ = shapeInfo[linkToJoin][5]
					
					MidPointX = (linkToJoinPointX[0]+linkToJoinPointX[1])/2
					MidPointY = (linkToJoinPointY[0]+linkToJoinPointY[1])/2
					MidPointZ = (linkToJoinPointZ[0]+linkToJoinPointZ[1])/2
					
					tempLocationMatrix = locationMatrix.copy()
					
					inner_flag1 = 0
					inner_flag2 = 0
					
					if jointPositionAxis == 0:
						minX = linkToJoinPointX[1]
						maxX = minX + length
						minY = MidPointY - width/2
						maxY = minY + width
						minZ = MidPointZ - height/2
						maxZ = minZ + height
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(math.ceil(maxX) - math.floor(minX)):
							for y2 in range(math.ceil(maxY) - math.floor(minY)):
								for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										
										if (locationMatrix[math.floor(x2 + linkToJoinPointX[1]), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] == 1):           
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										else:
											flag2 = 0
											
											tempLocationMatrix[math.floor(x2 + linkToJoinPointX[1]), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] = 1
											
											
											
											
									elif (locationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == 1):           
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									
									else:
										flag2 = 0
										
										tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
										
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
					elif jointPositionAxis == 1:
						minX = MidPointX - length/2
						maxX = minX + length
						minY = linkToJoinPointY[1]
						maxY = minY + width
						minZ = MidPointZ - height/2
						maxZ = minZ + height
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(math.ceil(maxX) - math.floor(minX)):
							for y2 in range(math.ceil(maxY) - math.floor(minY)):
								for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										
										if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(y2 + linkToJoinPointY[1]), math.floor(MidPointZ - height/2 + z2)] == 1):
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											
											tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(y2 + linkToJoinPointY[1]), math.floor(MidPointZ - height/2 + z2)] = 1
											
											
									# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
									elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == 1):
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									
									else:
										flag2 = 0
										
										tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] = 1
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
					elif jointPositionAxis == 2:
						minX = MidPointX - length/2
						maxX = minX + length
						minY = MidPointY - width/2
						maxY = minY + width
						minZ = linkToJoinPointZ[1]
						maxZ = minZ + height
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(math.ceil(maxX) - math.floor(minX)):
							for y2 in range(math.ceil(maxY) - math.floor(minY)):
								for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(z2 + linkToJoinPointZ[1])] == 1):                                            
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											
											tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(z2 + linkToJoinPointZ[1])] = 1
											
											
									# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
									elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == 1):                                            
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									else:
										flag2 = 0
										
										tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] = 1
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
					# Negative Axis
					elif jointPositionAxis == 3:
						
						maxX = linkToJoinPointX[0]
						minX = maxX - length
						minY = MidPointY - width/2
						maxY = minY + width
						minZ = MidPointZ - height/2
						maxZ = minZ + height
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(1,math.floor(maxX) - math.floor(minX)+1):
							for y2 in range(math.ceil(maxY) - math.floor(minY)):
								for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										
										if (locationMatrix[math.floor(linkToJoinPointX[0] - x2), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] == 1):           
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										else:
											flag2 = 0
											tempLocationMatrix[math.floor(linkToJoinPointX[0] - x2), math.floor(MidPointY - width/2 + y2), math.floor(MidPointZ - height/2 + z2)] = 1
											
											
									elif (locationMatrix[math.floor(linkToJoinPointX[0] - x2), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == 1):           
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									
									else:
										flag2 = 0
										tempLocationMatrix[math.floor(linkToJoinPointX[0] - x2), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
					elif jointPositionAxis == 4:
						minX = MidPointX - length/2
						maxX = minX + length
						maxY = linkToJoinPointY[0]
						minY = maxY - width
						minZ = MidPointZ - height/2
						maxZ = minZ + height
						
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(math.ceil(maxX) - math.floor(minX)):
							for y2 in range(1,math.floor(maxY) - math.floor(minY)+1):
								for z2 in range(math.ceil(maxZ) - math.floor(minZ)):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										
										if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.floor(MidPointZ - height/2 + z2)] == 1):
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.floor(MidPointZ - height/2 + z2)] = 1
											
											
									elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.ceil(MidPointZ - height/2 + z2)] == 1):
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									
									else:
										flag2 = 0
										tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.floor(linkToJoinPointY[0] - y2), math.ceil(MidPointZ - height/2 + z2)] = 1
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
					else:
						minX = MidPointX - length/2
						maxX = minX + length
						minY = MidPointY - width/2
						maxY = minY + width
						maxZ = linkToJoinPointZ[0]
						minZ = maxZ - height
						if (minX < 0) or (minY < 0) or (minZ < 0):
							flag2 = 1
							tempLocationMatrix = locationMatrix.copy()
							length, width, height, shape_choice = self.initialize_shape_and_dimensions()
							inner_flag1 = 1
							
						for x2 in range(math.ceil(maxX) - math.floor(minX)):
							for y2 in range(math.ceil(maxY) - math.floor(minY)):
								for z2 in range(1,math.floor(maxZ) - math.floor(minZ)+1):
									
									if (x2 == 0) or (y2 == 0) or (z2 == 0):
										if (locationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] == 1):                                            
											flag2 = 1
											tempLocationMatrix = locationMatrix.copy()
											inner_flag1 = 1
											break
										
										else:
											flag2 = 0
											
											tempLocationMatrix[math.floor(MidPointX - length/2 + x2), math.floor(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] = 1
											
											
									# if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
									elif (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] == 1):                                            
										flag2 = 1
										tempLocationMatrix = locationMatrix.copy()
										inner_flag1 = 1
										break
									else:
										flag2 = 0
										
										tempLocationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.floor(linkToJoinPointZ[1] - z2)] = 1
									if inner_flag1 == 1:
										inner_flag2 = 1
										flag2 = 1
										break
								if inner_flag2 == 1:
										break
								
								
			locationMatrix = tempLocationMatrix.copy()
			i = 0
			for l in shapesAdded:
				if ("Link" + str(i) in shapesAdded):
					i = i+1
					pass
				else:
					break
			print("Link" + str(i))
			locationMatrix = tempLocationMatrix.copy()
			shapeInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ], shape_choice]
			print(shapeInfo)
			shapesAdded.append("Link" + str(i))
			connections.append([jointPositionAxis,linkToJoin])  
			total_creature_connections[linkToJoin+"_"+"Link"+ str(i)] = jointPositionAxis
			print(total_creature_connections)
			self.connections = connections
			sensorNeuronList.append(random.randint(0,1))
			
			
			
			
			
			
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		self.sensorNeuronList = sensorNeuronList
		self.shapesAdded = shapesAdded
		self.locationMatrix = locationMatrix.copy()
		self.connections = connections
		
		numSensorNeurons = sensorNeuronList.count(1)
		randomRow =  random.randint(0,numSensorNeurons - 1)
		
		numLinks = len(shapesAdded)
		randomColumn = random.randint(0,numLinks - 1)
		self.weights[randomRow,randomColumn] =  random.random() * 2 - 1
		
		
	def Set_ID(self, nextAvailableID):
		self.myID = nextAvailableID
		pass
		
		
		
		