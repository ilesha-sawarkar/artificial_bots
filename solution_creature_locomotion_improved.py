#!/usr/bin/env python3

import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import time
import constants as c
import pybullet as p
import math



class SOLUTION:
	def __init__(self, ID):
			#self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
		
			self.weights=0
			self.myID= ID
			self.motorNeurons=[]
			self.numSensorNeurons=0
			self.numMotorNeurons=0
			self.sensorNeuronsLinkNames=[]
			self.sensorNeurons=[]
			self.LinkJointLink = []
			self.locationMatrix = np.zeros((80,80,80,3))
		
			self.shapeInfo = {}
			self.shapesAdded = []  #linksAdded
			self.total_connections = []
			self.creature_final_Connections = {}  #grandConnections
		
		
	def Evaluate(self,directOrGui ):
		self.Create_World()
		self.Create_Brain()
		self.Create_Body()
		
		os.system(f"python3 simulate.py {directOrGui} {self.myID} &")
		
		
		while not os.path.exists(f"data/fitness{self.myID}.txt"):
				time.sleep(0.001)
		fit_file = open(f"data/fitness{self.myID}.txt", "r")
		
		fitness = fit_file.read()
		self.fitness = float(fitness)	
		os.system(f"rm data/fitness{self.myID}.txt")
		print(self.fitness)
		
	def Set_ID(self):
		self.myID += 1
		
	def Start_Simulation(self, directOrGui):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system(f"python3 simulate.py {directOrGui} {self.myID}   &")
		
	def Wait_For_Simulation_To_End(self):
		while not os.path.exists(f"data/fitness{self.myID}.txt"):
			time.sleep(0.01)
		fit_file = open(f"data/fitness{self.myID}.txt", "r")
		fitness = fit_file.read()
		if fitness == '':
			
			time.sleep(0.1)
			fitness = fit_file.read()
		self.fitness = float(fitness)
		print('Fitness: ', self.fitness)
		fit_file.close()
		os.system(f"rm data/fitness{self.myID}.txt")
		
		
	def Mutate(self):
		self.numSensorNeurons= c.numSensorNeurons.count(1)
		self.numMotorNeurons = len(self.motorNeurons)
		
		row = random.randint(0,self.numSensorNeurons-1)
		col = random.randint(0,self.numMotorNeurons-1)
		self.weights[row][col]  =  random.random() * 2 - 1
		
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		length = 1
		width = 1
		height = 1
		x = -10
		y = 5
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
			
			
			
	def Create_Child_Body(self):
		pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
		
		shapeInfo = self.shapeInfo
		creature_final_Connections =  self.creature_final_Connections
		sensorNeuronsList = self.sensorNeurons
		linksAdded = self.shapesAdded
		child_joints = creature_final_Connections.keys()
		
		shapes=['cube', 'sphere']
		
		counter = 0
		
		for link in linksAdded:
			length = shapeInfo[link][0]
			width = shapeInfo[link][1]
			height = shapeInfo[link][2]
			shape_choice=shapeInfo[link][3]
			
			
			if (sensorNeuronsList[counter] == 0):
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
			if (link == "Link0"):
				self.Send_Shape(shape_choice, name = link, pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				#pyrosim.Send_Cube(name = link, pos=[length/2,width/2,height/2] , size=[length,width,height], mass = 1, tag = tag, color = [r, g, b ,a ] )
				counter += 1
			else:
				for j in child_joints:
					if ("_" + link) in j:
						jointPositionAxis = creature_final_Connections[j]
						linkToJoin = j[0:j.find("_")]
						break
					
				for k in child_joints:
					if ("_" + linkToJoin) in k:
						grandParAxis = creature_final_Connections[k]
						
				# Joints   
				if (linkToJoin == "Link0"):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0], shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1], shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
						
				elif(grandParAxis == jointPositionAxis):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0],0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [0,shapeInfo[linkToJoin][1],0], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0,0,shapeInfo[linkToJoin][2]], jointAxis = "0 0 1")
						
				else:
					if (grandParAxis == 0):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
					elif (grandParAxis == 1):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, shapeInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
					else:
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + link , parent = linkToJoin , child = link , type = "revolute", position = [shapeInfo[linkToJoin][0]/2, 0,  shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + link, parent = linkToJoin  , child = link , type = "revolute", position = [0, shapeInfo[linkToJoin][1]/2, shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
							
				# Next link
				if (jointPositionAxis == 0):
					self.Send_Shape(shape_choice, name = link + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					#pyrosim.Send_Cube(name = link, pos=[length/2,0,0] , size=[length,width,height], mass = 1, tag = tag, color = [r, g, b ,a ])
				elif (jointPositionAxis == 1):
					self.Send_Shape(shape_choice, name = link + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					#pyrosim.Send_Cube(name = link, pos=[0,width/2,0] , size=[length,width,height], mass = 1, tag = tag, color = [r, g, b ,a ])
				else:
					self.Send_Shape(shape_choice, name = link + str(i), pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
					
				counter += 1
				# flag2 = 1
				
		self.shapeInfo = shapeInfo
		self.creature_final_Connections = creature_final_Connections
		self.sensorNeuronsList = sensorNeuronsList
		self.shapesAdded = shapesAdded
		pyrosim.End()
		
			
			
			
	def Create_Body(self):
		pyrosim.Start_URDF(f"body/body{self.myID}.urdf")
		
		self.shapeInfo = {}
		self.shapesAdded = []
		self.total_connections = []
		self.creature_final_Connections = {}
		
		minX = 0
		minY = 0
		minZ = 0
		
		maxX = 0
		maxY = 0
		maxZ = 0
		
		number_of_links= random.randint(3,c.maxLinks)
		self.sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]
		print(self.sensorNeurons)
		
		shapes=['cube', 'sphere']
		
		
		
		
		
		for i in range(0,number_of_links):
			length = random.uniform(0.8,2) 
			width = random.uniform(0.8,2) 
			height = random.uniform(0.8,2) 
			shape_choice=random.choice(shapes)
			
			flag2=1
			if self.sensorNeurons[i]==0: #No Sensor
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
				
			if shape_choice=='sphere':
				length=(width/2)
				height=(width/2)
				width=width
				
				
			if (i == 0):
				self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				minX = 0
				minY = 0
				minZ = 0
				
				
				for x in range(math.ceil(length)):
					for y in range(math.ceil(width)):
						for z in range(math.ceil(height)):
							self.locationMatrix[20+x,20+y,0+z] = 1
							maxX = 20+x
							maxY = 20+y
							maxZ = 0+z
							#else:
							#	pass
				
			if(i == 0):
				self.shapeInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ], [shape_choice]]
				self.shapesAdded.append("Link" + str(i))
				
			else:
				while(flag2 == 1):
					jointPositionAxis = random.choice([0, 1, 2])
					# jointPositionAxis = random.choice([0, 1])
					# jointPositionAxis = 0
					linkToJoin = random.choice(self.shapesAdded)
					
					if ([jointPositionAxis,linkToJoin] not in self.total_connections ):
						linkToJoinPointX = self.shapeInfo[linkToJoin][3]
						linkToJoinPointY = self.shapeInfo[linkToJoin][4]
						linkToJoinPointZ = self.shapeInfo[linkToJoin][5]
						
						MidPointX = (linkToJoinPointX[0]+linkToJoinPointX[1])/2
						MidPointY = (linkToJoinPointY[0]+linkToJoinPointY[1])/2
						MidPointZ = (linkToJoinPointZ[0]+linkToJoinPointZ[1])/2
						
						tempLocationMatrix =self.locationMatrix.copy()
						positionTaken = np.array([1,1,1])
						if jointPositionAxis == 0:
							for x2 in range(math.ceil(length)):
								for y2 in range(math.ceil(width)):
									for z2 in range(math.ceil(height)):
										
										
										if (self.locationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
											flag2 = 1
											tempLocationMatrix = self.locationMatrix.copy()
											
											break
										else:
											flag2 = 0
											minX = linkToJoinPointX[1]
											maxX = minX + length
											minY = MidPointY - width/2
											maxY = minY + width
											minZ = MidPointZ - height/2
											maxZ = minZ + height
											tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
											
											
						elif jointPositionAxis == 1:
							for x2 in range(math.ceil(length)):
								for y2 in range(math.ceil(width)):
									for z2 in range(math.ceil(height)):
										
										if (self.locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
											flag2 = 1
											tempLocationMatrix = self.locationMatrix.copy()
											
											break
										else:
											flag2 = 0
											minX = MidPointX - length/2
											maxX = minX + length
											minY = linkToJoinPointY[1]
											maxY = minY + width
											minZ = MidPointZ - height/2
											maxZ = minZ + height
											tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
											
						else:
							for x2 in range(math.ceil(length)):
								for y2 in range(math.ceil(width)):
									for z2 in range(math.ceil(height)):
										
										if (self.locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
											flag2 = 1
											tempLocationMatrix = self.locationMatrix.copy()
											break
										else:
											flag2 = 0
											minX = MidPointX - length/2
											maxX = minX + length
											minY = MidPointY - width/2
											maxY = minY + width
											minZ = linkToJoinPointZ[1]
											maxZ = minZ + height
											tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
											
				self.locationMatrix = tempLocationMatrix.copy()
				
				
				self.shapeInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ], [shape_choice]]
				
				
				self.shapesAdded.append("Link" + str(i))
				self.total_connections.append([jointPositionAxis,linkToJoin])  
				self.creature_final_Connections[linkToJoin+"_"+"Link"+ str(i)] = jointPositionAxis
				# print(grandConnections)
				
				# LinkJointLinkRev = self.LinkJointLink.copy()
				# LinkJointLinkRev = LinkJointLinkRev.reverse()
				# print(LinkJointLinkRev, "reversed")
				for link in reversed(range(len(self.LinkJointLink))) :
					if ("_"+linkToJoin) in self.LinkJointLink[link]:
						grandparentLink = self.LinkJointLink[link]
						grandParAxis = self.creature_final_Connections[grandparentLink]
						break
					
					
				if (linkToJoin == "Link0"):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, self.shapeInfo[linkToJoin][1], self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, self.shapeInfo[linkToJoin][1], self.shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, self.shapeInfo[linkToJoin][1], self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
						
				elif(grandParAxis == jointPositionAxis):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2,0,0], jointAxis = "1 0 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [0,self.shapeInfo[linkToJoin][1]/2,0], jointAxis = "0 1 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					else:
						pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0,0,self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
						self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
						
				else:
					if (grandParAxis == 0):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, self.shapeInfo[linkToJoin][1], 0], jointAxis = "0 1 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, 0, self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					elif (grandParAxis == 1):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, self.shapeInfo[linkToJoin][1], 0], jointAxis = "1 0 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, self.shapeInfo[linkToJoin][1]/2, self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
					else:
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [self.shapeInfo[linkToJoin][0]/2, 0,  self.shapeInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
						else:
							pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, self.shapeInfo[linkToJoin][1]/2, self.shapeInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
							self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
							
							
							
							
							
							
							
				if (jointPositionAxis == 0):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPositionAxis == 1):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				else:
					self.Send_Shape(shape_choice, name = "Link" + str(i),  pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				self.LinkJointLink.append(linkToJoin + "_" + "Link" + str(i))
				# print(self.LinkJointLink, "straight")
				flag2 = 1
				
				
				
		print('Generated_new')		
		pyrosim.End()
		
	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain/brain{self.myID}.nndf")
		self.numSensorNeurons=self.sensorNeurons.count(1)
		self.numMotorNeurons = len(self.motorNeurons)
		self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
		print(self.numSensorNeurons,self.numMotorNeurons)
		print("synapse_weights: ", self.weights)
		
		i=0
		for link in self.sensorNeurons:
			if link==1:
				pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link"+str(i))
				i+=1
				
		print(self.motorNeurons)
		for joint in self.motorNeurons:
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
			pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
			
			counter = 0
			numLinks = len(self.linksAdded)
			for i in range(0,numLinks):
				if (self.randSensorsList[i] == 1):
					pyrosim.Send_Sensor_Neuron(name = counter , linkName = self.linksAdded[i])
					counter += 1
					
			child_LinkJointLink = self.creature_final_Connections.keys()
			listLJL = list(child_LinkJointLink)
			self.numSensorNeurons=self.sensorNeurons.count(1)
			for j in range(0,numLinks - 1):
				pyrosim.Send_Motor_Neuron( name = j + self.numSensorNeurons  , jointName = listLJL[j])
				
			for currentRow in range(0,self.numSensorNeurons):
				for currentColumn in range(0, self.numMotorNeurons):
					
					pyrosim.Send_Synapse( 
						sourceNeuronName = currentRow , 
						targetNeuronName = currentColumn+ self.numSensorNeurons , 
						weight = self.weights[currentRow][currentColumn] )						
			pyrosim.End()
		
		
		
		
		