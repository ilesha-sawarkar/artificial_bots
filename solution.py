#!/usr/bin/env python3

import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import time
import constants as c
import math
from collections import Counter


np.random.seed(c.numpyseed)
random.seed(c.randomseed)

class SOLUTION:
	def __init__(self, ID):
		self.weights=0
		self.myID= ID
		self.motorNeurons=[]
		self.numSensorNeurons=0
		self.numMotorNeurons=0
		self.shapeInfo = []
		self.total_creature_connections = {}
		self.sensorNeuronList =[]
		self.linksAdded = []
		self.locationMatrix = np.zeros((40,40,40,3))
		self.connections = []
		self.LinkJoints=[]
		
#	def Evaluate(self,directOrGui ):
#		self.Create_World()
#		self.Create_Brain()
#		self.Create_Body()
#		
#		os.system(f"python3 simulate.py {directOrGui} {self.myID} &")
#		
#		
#		while not os.path.exists(f"data/fitness{self.myID}.txt"):
#				time.sleep(0.001)
#		fit_file = open(f"data/fitness{self.myID}.txt", "r")
#		
#		fitness = fit_file.read()
#		self.fitness = float(fitness)	
#		os.system(f"rm data/fitness{self.myID}.txt")
#		print(self.fitness)
		
	def Set_ID(self):
		self.myID += 1
	
	def Start_Simulation(self, directOrGui, child_true=0):
		self.Create_World()
		if (child_true == 1):
			self.Create_Child_Body()
			self.Create_Child_Brain()
		else:
			self.Create_Body()
			self.Create_Brain()
			
		os.system("python3 simulate.py " + str(directOrGui) + " " + str(self.myID) + " &")  #2>1
		
	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("data/fitness"+str(self.myID)+".txt"):
			time.sleep(0.01)
		fit_file = open("fitness"+str(self.myID)+".txt", "r")
		fitness = fit_file.read()
		if fitness == '':
			
			time.sleep(0.1)
			fitness = fit_file.read()
		self.fitness = float(fitness)
		print('Fitness: ', self.fitness)
		fit_file.close()
		os.system("fitness"+str(self.myID)+".txt")
		return(self.fitness)
		
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
	
	def Mutate(self):
		shapeInfo = self.shapeInfo
		total_creature_connections =  self.total_creature_connections
		sensorNeuronList = self.sensorNeuronList
		shapesAdded = self.shapesAdded
		child_links = total_creature_connections.keys()
		#list_child_links = list(child_links)
		locationMatrix = self.locationMatrix
		connections = self.connections
		Joint= self.Joint
		
		add_remove_none = 2
		if len(list(child_links)) > 3:
			add_remove_none = random.choice([0, 1, 2])
			# add_remove_none = 0
			
		# Remove Link
		# 0 - Remove Link/ 1 - Add Link/ 2 - None
		if (add_remove_none == 0):
			LinksWithChild = []
			for link in shapesAdded:
				for j in list(child_links):
						if (link + "_" ) in j:
							LinksWithChild.append(link)
			childlessLinks = list((Counter(shapesAdded)-Counter(LinksWithChild)).elements())
			linkToRemove = random.choice(childlessLinks)
			shapesAdded.remove(linkToRemove)
			del shapesAdded[linkToRemove]
			
			#fix this
			sensorNeuronList.pop()
			
			for link_joint in list(child_links):
				if("_" + linkToRemove) in link_joint:
					child_links = link_joint
					break
				
			# del LinkJoiNtLink[LinkJoitLinkToRemove]
			del total_creature_connections[child_links]
			
		elif (add_remove_none==1):
			sensor_val=random.randint(0,1)
			sensorNeuronList.append(sensor_val)			
			length = random.randint(1,2) 
			width = random.randint(1,2) 
			height = random.randint(1,2) 
			shapes=['sphere', 'cube']
			
			shape_choice=random.choice(shapes) #shape chosen for each link
			
			if sensor_val==0: #No Sensor
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
				
			if shape_choice=='sphere':
				length=int((width/2))
				height=int((width/2))
				width=width
			
			while(flag2==1):
				
				
				jointPosition_Direction = random.choice([0,1,2])
				
				JoiningLink= random.choice(shapesAdded)  #ranndomly choose a link to add a joint to
				
				if ([jointPosition_Direction, JoiningLink ] not in connections):
					JoiningLink_X_MaxMin= shapeInfo[JoiningLink][1]
					JoiningLink_Y_MaxMin= shapeInfo[JoiningLink][2]
					JoiningLink_Z_MaxMin= shapeInfo[JoiningLink][3]
					
					MidPointX = (JoiningLink_X_MaxMin[0]+JoiningLink_X_MaxMin[1])/2
					MidPointY = (JoiningLink_Y_MaxMin[0]+JoiningLink_Y_MaxMin[1])/2
					MidPointZ = (JoiningLink_Z_MaxMin[0]+JoiningLink_Z_MaxMin[1])/2
					
					tempLocationMatrix = location_Matrix.copy()
					
					positionTaken = np.array([1,1,1])
					
					if jointPosition_Direction ==0:
						for x in range(length):
							for y in range(width):
								for z in range(height):
									if (location_Matrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - y /2), math.ceil(MidPointZ - height/2 + z )] == positionTaken).all():
										flag2=1
										tempLocationMatrix=location_Matrix.copy()
										break
									else:
										flag2=0
										
										minimumX=MidPointX -length/2
										maximumX=minimumX+length
										
										minimumY=JoiningLink_Y_MaxMin[1]
										maximumY=minimumY+width
										
										minimumZ=MidPointZ - height/2
										maximumZ=MidPointZ - height/2
										tempLocationMatrix[math.ceil(x+ JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
										
					elif jointPosition_Direction ==1:
						for x in range(length):
							for y in range(width):
								for z in range(height):
									if (location_Matrix[math.ceil(MidPointX - length/2 + x), math.ceil(y  + JoiningLink_Y_MaxMin[1]), math.ceil(MidPointZ - height/2 + z )] == positionTaken).all():
										flag2=1
										tempLocationMatrix=location_Matrix.copy()
										break
									else:
										flag2=0
										
										minimumX=MidPointX -length/2
										maximumX=minimumX+length
										
										minimumY=JoiningLink_Y_MaxMin[1]
										maximumY=minimumY+width
										
										minimumZ=MidPointZ - height/2
										maximumZ=MidPointZ - height/2
										tempLocationMatrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
										
					elif jointPosition_Direction ==2:
						for x in range(length):
							for y in range(width):
								for z in range(height):
									if (location_Matrix[ math.ceil(MidPointX - length/2 + x), math.ceil(y + JoiningLink_Y_MaxMin[1]), math.ceil(JoiningLink_Z_MaxMin[1])] == positionTaken).all():
										flag2=1
										tempLocationMatrix=location_Matrix.copy()
										break
									else:
										flag2=0
										
										minimumX=MidPointX -length/2
										maximumX=minimumX+length
										
										minimumY=MidPointY -width/2
										maximumY=minimumY+width
										
										minimumZ=JoiningLink_Z_MaxMin[1]
										maximumZ=minimumZ + height
										tempLocationMatrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
										
		location_Matrix= tempLocationMatrix.copy()
		
		shapeInfo["Link" + str(i)] = [[length,width,height], [minimumX, maximumX], [minimumY, maximumY], [minimumZ, maximumZ], shape_choice]
		
		shapesAdded.append("Link" + str(i))
		connections.append([jointPosition_Direction, JoiningLink])
		
		total_creature_connections[JoiningLink+"_"+"Link" + str(i)]=jointPosition_Direction
		self.connections= connections
		
		
		for link in reversed(range(len(self.LinkJoints))):
			if ("_"+JoiningLink) in self.LinkJoints[link]:
				grandparentLink = self.LinkJoints[link]
				grandParAxis = total_creature_connections[grandparentLink]
				break
			
		if(JoiningLink == "Link0"):
			if(jointPosition_Direction==0):
				pyrosim.Send_Joint(
					name=JoiningLink+"_"+"Link" + str(i), 
					parent=JoiningLink, 
					child="Link" + str(i), type="revolute",
					position=[shapeInfo[JoiningLink][0], 
						shapeInfo[JoiningLink][0][1]/2,
						shapeInfo[JoiningLink][0][2]/2],
					jointAxis="1 0 0")
			elif(jointPosition_Direction==1):
				pyrosim.Send_Joint(
					name=JoiningLink+"_"+"Link" + str(i), 
					parent=JoiningLink, 
					child="Link" + str(i), type="revolute",
					position=[shapeInfo[JoiningLink][0][0]/2 , 
						shapeInfo[JoiningLink][0][1],
						shapeInfo[JoiningLink][0][2]/2],
					jointAxis="0 1 0")
			elif(jointPosition_Direction==2):
				pyrosim.Send_Joint(
					name=JoiningLink+"_"+"Link" + str(i), 
					parent=JoiningLink, 
					child="Link" + str(i), type="revolute",
					position=[shapeInfo[JoiningLink][0][0]/2 , 
						shapeInfo[JoiningLink][0][1]/2,
						shapeInfo[JoiningLink][0][2]],
					jointAxis="0 0 1")
				
		elif(grandParAxis == jointPosition_Direction):
			if (jointPosition_Direction == 0):
				pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[JoiningLink][0][0],0,0], jointAxis = "1 0 0")
			elif (jointPosition_Direction == 1):
				pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [0,shapeInfo[JoiningLink][0][1],0], jointAxis = "0 1 0")
			elif (jointPosition_Direction == 2):
				pyrosim.Send_Joint(name = shapeInfo + "_" + "Link" + str(i) , parent = JoiningLink  , child = "Link" + str(i) , type = "revolute", position = [0,0, shapeInfo[JoiningLink][0][2]], jointAxis = "0 0 1")
				
		else:
			if (grandParAxis == 0):
				if (jointPosition_Direction == 1):
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [
						shapeInfo[JoiningLink][0][0]/2,
						shapeInfo[JoiningLink][0][1]/2,
						0], jointAxis = "0 1 0")
				else:
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , 
						child = "Link" + str(i) ,
						type = "revolute", 
						position = [shapeInfo[JoiningLink][0][0]/2,
							0,
							shapeInfo[JoiningLink][0][2]/2], 
						jointAxis = "0 0 1")
					
			elif (grandParAxis == 1):
				if (jointPosition_Direction == 0):
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
						parent = JoiningLink , 
						child = "Link" + str(i) , 
						type = "revolute",
						position = [shapeInfo[JoiningLink][0][0]/2,
						shapeInfo[JoiningLink][0][1]/2,
						0], jointAxis = "0 1 0")
				else:
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
						parent = JoiningLink , 
						child = "Link" + str(i) , 
						type = "revolute",
						position = [0, 
							shapeInfo[JoiningLink][0][1]/2,
							shapeInfo[JoiningLink][0][2]/2], 
						jointAxis = "0 0 1")
			else:
				if (jointPosition_Direction == 0):
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
						parent = JoiningLink , 
						child = "Link" + str(i) , 
						type = "revolute",
						position = [
							shapeInfo[JoiningLink][0][0]/2,
							0, 
							shapeInfo[JoiningLink][0][2]/2], 
						jointAxis = "1 0 0")
				else:
					pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
						parent = JoiningLink , 
						child = "Link" + str(i) , 
						type = "revolute",
						position = [0, 
							shapeInfo[JoiningLink][0][1]/2,
							shapeInfo[JoiningLink][0][2]/2], 
						jointAxis = "0 0 1")
					
		if (jointPosition_Direction == 0):
			self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
		elif (jointPosition_Direction == 1):
			self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
			
		else:
			self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
#		self.shapeInfo = shapeInfo
#		self.total_creature_connections = total_creature_connections
#		self.shapesAdded = shapesAdded
			
			
			
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		self.sensorNeuronList = sensorNeuronList
		self.shapesAdded = shapesAdded
		
		self.numSensorNeurons = sensorNeuronList.count(1)
		#self.numMotorNeurons = len(self.motorNeurons)
		
		row =  random.randint(0,self.numSensorNeurons - 1)
		
		numLinks = len(shapesAdded)
		col = random.randint(0,numLinks - 1)
		self.weights[row][col]  =  random.random() * 2 - 1		
		
	
	
	def Send_Shape(self, shape, name, pos, size, mass, material_name , rgba):
		print(shape)
		if shape=='sphere':
			radius=[size[1]/2] #initializing the random assigned width as radius length
			print("Sphere :",radius)
			pyrosim.Send_Sphere(name=name , pos= pos, size=radius, mass=mass, material_name=material_name, rgba=rgba)
		elif shape=='cube':
			pyrosim.Send_Cube(name=name , pos= pos, size=size, mass=mass, material_name=material_name, rgba=rgba)
		
		
	def Create_Body(self):
		pyrosim.Start_URDF("body/body"+str(self.myID)+".urdf")
		
		shapeInfo = {}
		shapesAdded = []
		total_creature_connections = {}
		connections = []
		self.sensorNeuronList=[]
		self.LinkJoints=[]
		location_Matrix=self.locationMatrix
		shape_List=['sphere'] #, 'cube'
		
		
		number_of_links= random.randint(3,c.maxLinks)
		self.sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]
		print(self.sensorNeurons)
		
#		minimumX=0
#		minimumY=0
#		minimumZ=0
#		
#		maximumX=0
#		maximumY=0
#		maximumZ=0
		
		for i in range (0, number_of_links):
			length = random.randint(1,2) 
			width = random.randint(1,2) 
			height = random.randint(1,2) 
			
			shape_choice=random.choice(shape_List) #shape chosen for each link
			
			
			if self.sensorNeurons[i]==0: #No Sensor
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
				
			if shape_choice=='sphere':
				length=int((width/2))
				height=int((width/2))
				width=width
				
			if (i == 0):
				self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				
				minimumX=0
				minimumY=0
				minimumZ=0
				for x in range(length):
					for y in range(width):
						for z in range(height):
							location_Matrix[10+x, 20+y , 0+height]=1
							
							maximumX=20+length
							maximumY=20+width
							maximumZ=0 +z 
							
			if(i == 0):
				
				shapeInfo["Link" + str(i)]=[[length,width,height], [minimumX, maximumX], [minimumY, maximumY], [minimumZ, maximumZ], shape_choice]
				
				shapesAdded.append("Link" + str(i))
				flag2=1
				
			else:
				while(flag2==1):
					
					
					jointPosition_Direction = random.choice([0,1,2])
					
					JoiningLink= random.choice(shapesAdded)  #ranndomly choose a link to add a joint to
					
					if ([jointPosition_Direction, JoiningLink ] not in connections):
						JoiningLink_X_MaxMin= shapeInfo[JoiningLink][1]
						JoiningLink_Y_MaxMin= shapeInfo[JoiningLink][2]
						JoiningLink_Z_MaxMin= shapeInfo[JoiningLink][3]
						
						MidPointX = (JoiningLink_X_MaxMin[0]+JoiningLink_X_MaxMin[1])/2
						MidPointY = (JoiningLink_Y_MaxMin[0]+JoiningLink_Y_MaxMin[1])/2
						MidPointZ = (JoiningLink_Z_MaxMin[0]+JoiningLink_Z_MaxMin[1])/2
						
						tempLocationMatrix = location_Matrix.copy()
						
						positionTaken = np.array([1,1,1])
						
						if jointPosition_Direction ==0:
							for x in range(length):
								for y in range(width):
									for z in range(height):
										if (location_Matrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - y /2), math.ceil(MidPointZ - height/2 + z )] == positionTaken).all():
											flag2=1
											tempLocationMatrix=location_Matrix.copy()
											break
										else:
											flag2=0
											
											minimumX=MidPointX -length/2
											maximumX=minimumX+length
											
											minimumY=JoiningLink_Y_MaxMin[1]
											maximumY=minimumY+width
											
											minimumZ=MidPointZ - height/2
											maximumZ=MidPointZ - height/2
											tempLocationMatrix[math.ceil(x+ JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
											
						elif jointPosition_Direction ==1:
							for x in range(length):
								for y in range(width):
									for z in range(height):
										if (location_Matrix[math.ceil(MidPointX - length/2 + x), math.ceil(y  + JoiningLink_Y_MaxMin[1]), math.ceil(MidPointZ - height/2 + z )] == positionTaken).all():
											flag2=1
											tempLocationMatrix=location_Matrix.copy()
											break
										else:
											flag2=0
											
											minimumX=MidPointX -length/2
											maximumX=minimumX+length
											
											minimumY=JoiningLink_Y_MaxMin[1]
											maximumY=minimumY+width
											
											minimumZ=MidPointZ - height/2
											maximumZ=MidPointZ - height/2
											tempLocationMatrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
											
						elif jointPosition_Direction ==2:
							for x in range(length):
								for y in range(width):
									for z in range(height):
										if (location_Matrix[ math.ceil(MidPointX - length/2 + x), math.ceil(y  + JoiningLink_Y_MaxMin[1]), math.ceil(JoiningLink_Z_MaxMin[1])] == positionTaken).all():
											flag2=1
											tempLocationMatrix=location_Matrix.copy()
											break
										else:
											flag2=0
											
											minimumX=MidPointX -length/2
											maximumX=minimumX+length
											
											minimumY=MidPointY -width/2
											maximumY=minimumY+width
											
											minimumZ=JoiningLink_Z_MaxMin[1]
											maximumZ=minimumZ + height
											tempLocationMatrix[math.ceil(x + JoiningLink_X_MaxMin[1]), math.ceil(MidPointY - width/2 +y ), math.ceil(MidPointZ - height/2 +z )]=1
											
				location_Matrix= tempLocationMatrix.copy()
				
				shapeInfo["Link" + str(i)] = [[length,width,height], [minimumX, maximumX], [minimumY, maximumY], [minimumZ, maximumZ], shape_choice]
				
				shapesAdded.append("Link" + str(i))
				connections.append([jointPosition_Direction, JoiningLink])
				
				total_creature_connections[JoiningLink+"_"+"Link" + str(i)]=jointPosition_Direction
				self.connections= connections
				#Joints=self.Joints
				no_joints= len(self.LinkJoints)
				
				for link in reversed(range(no_joints)):
					if ("_"+JoiningLink) in self.LinkJoints[link]:
						grandparentLink = self.LinkJoints[link]
						grandParAxis = total_creature_connections[grandparentLink]
						break
					
				if(JoiningLink == "Link0"):
					if(jointPosition_Direction==0):
						pyrosim.Send_Joint(
							name=JoiningLink+"_"+"Link" + str(i), 
							parent=JoiningLink, 
							child="Link" + str(i), type="revolute",
							position=[shapeInfo[JoiningLink][0][0], 
								shapeInfo[JoiningLink][0][1]/2,
								shapeInfo[JoiningLink][0][2]/2],
							jointAxis="1 0 0")
					elif(jointPosition_Direction==1):
						pyrosim.Send_Joint(
							name=JoiningLink+"_"+"Link" + str(i), 
							parent=JoiningLink, 
							child="Link" + str(i), type="revolute",
							position=[shapeInfo[JoiningLink][0][0]/2 , 
								shapeInfo[JoiningLink][0][1],
								shapeInfo[JoiningLink][0][2]/2],
							jointAxis="0 1 0")
					elif(jointPosition_Direction==2):
						pyrosim.Send_Joint(
							name=JoiningLink+"_"+"Link" + str(i), 
							parent=JoiningLink, 
							child="Link" + str(i), type="revolute",
							position=[shapeInfo[JoiningLink][0][0]/2 , 
								shapeInfo[JoiningLink][0][1]/2,
								shapeInfo[JoiningLink][0][2]],
							jointAxis="0 0 1")
						
				elif(grandParAxis == jointPosition_Direction):
					if (jointPosition_Direction == 0):
						pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [shapeInfo[JoiningLink][0][0],0,0], jointAxis = "1 0 0")
					elif (jointPosition_Direction == 1):
						pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [0,shapeInfo[JoiningLink][0][1],0], jointAxis = "0 1 0")
					elif (jointPosition_Direction == 2):
						pyrosim.Send_Joint(name = shapeInfo + "_" + "Link" + str(i) , parent = JoiningLink  , child = "Link" + str(i) , type = "revolute", position = [0,0, shapeInfo[JoiningLink][0][2]], jointAxis = "0 0 1")
						
				else:
					if (grandParAxis == 0):
						if (jointPosition_Direction == 1):
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , child = "Link" + str(i) , type = "revolute", position = [
								shapeInfo[JoiningLink][0][0]/2,
								shapeInfo[JoiningLink][0][1]/2,
								0], jointAxis = "0 1 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , parent = JoiningLink , 
								child = "Link" + str(i) ,
								type = "revolute", 
								position = [shapeInfo[JoiningLink][0][0]/2,
									0,
									shapeInfo[JoiningLink][0][2]/2], 
								jointAxis = "0 0 1")
							
					elif (grandParAxis == 1):
						if (jointPosition_Direction == 0):
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
								parent = JoiningLink , 
								child = "Link" + str(i) , 
								type = "revolute",
								position = [shapeInfo[JoiningLink][0][0]/2,
								shapeInfo[JoiningLink][0][1]/2,
								0], jointAxis = "0 1 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
								parent = JoiningLink , 
								child = "Link" + str(i) , 
								type = "revolute",
								position = [0, 
									shapeInfo[JoiningLink][0][1]/2,
									shapeInfo[JoiningLink][0][2]/2], 
								jointAxis = "0 0 1")
					else:
						if (jointPosition_Direction == 0):
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
								parent = JoiningLink , 
								child = "Link" + str(i) , 
								type = "revolute",
								position = [
									shapeInfo[JoiningLink][0][0]/2,
									0, 
									shapeInfo[JoiningLink][0][2]/2], 
								jointAxis = "1 0 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + "Link" + str(i) , 
								parent = JoiningLink , 
								child = "Link" + str(i) , 
								type = "revolute",
								position = [0, 
									shapeInfo[JoiningLink][0][1]/2,
									shapeInfo[JoiningLink][0][2]/2], 
								jointAxis = "0 0 1")
							
				if (jointPosition_Direction == 0):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPosition_Direction == 1):
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				else:
					self.Send_Shape(shape_choice, name = "Link" + str(i), pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
				self.LinkJoints.append(JoiningLink + "_" + "Link" + str(i))
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		self.shapesAdded = shapesAdded
		print("newGenerated")
		
		
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
		
	def Create_Child_Body(self):
		pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
		
		shapeInfo = self.shapeInfo
		total_creature_connections =  self.total_creature_connections
		sensorNeuronsList = self.sensorNeuronsList
		shapesAdded = self.shapesAdded
		child_joints = total_creature_connections.keys()
		
		#shapes=['cube', 'sphere']
		
		counter = 0
		
		for link in linksAdded:
			length = shapeInfo[link][0][0]
			width = shapeInfo[link][0][1]
			height = shapeInfo[link][0][2]
			shape_choice=shapeInfo[link][3]
			
			
			if (sensorNeuronsList[counter] == 0):
				color_name=c.color_No_Sensor_Link
				rgba_string=c.rgba_No_Sensor_Link 
			else:
				color_name=c.color_Sensor_Link
				rgba_string=c.rgba_Sensor_Link 
			if (link == "Link0"):
				self.Send_Shape(shape_choice, name = link, pos=[length/2,width/2,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				counter += 1
			else:
				for j in child_joints:
					if ("_" + link) in j:
						jointPositionAxis = total_creature_connections[j]
						JoiningLink = j[0:j.find("_")]
						break
					
				for k in child_joints:
					if ("_" + JoiningLink) in k:
						grandParAxis = total_creature_connections[k]
						
				# Joints   
				if (JoiningLink == "Link0"):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = JoiningLink + "_" + link , 
							parent = JoiningLink , 
							child = link , 
							type = "revolute", 
							position = [shapeInfo[JoiningLink][0], shapeInfo[JoiningLink][1]/2, 
								shapeInfo[JoiningLink][2]/2], 
							jointAxis = "1 0 0")
						
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = JoiningLink + "_" + link ,
							parent = JoiningLink , 
							child = link ,
							type = "revolute", 
							position = [shapeInfo[JoiningLink][0]/2, shapeInfo[JoiningLink][1], 
								shapeInfo[JoiningLink][2]/2], 
							jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0]/2, shapeInfo[JoiningLink][1]/2, shapeInfo[JoiningLink][2]], jointAxis = "0 0 1")
						
				elif(grandParAxis == jointPositionAxis):
					if (jointPositionAxis == 0):
						pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0],0,0], jointAxis = "1 0 0")
					elif (jointPositionAxis == 1):
						pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [0,shapeInfo[JoiningLink][1],0], jointAxis = "0 1 0")
					else:
						pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink  , child = link , type = "revolute", position = [0,0,shapeInfo[JoiningLink][2]], jointAxis = "0 0 1")
						
				else:
					if (grandParAxis == 0):
						if (jointPositionAxis == 1):
							pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0]/2, shapeInfo[JoiningLink][1]/2, 0], jointAxis = "0 1 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink  , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0]/2, 0, shapeInfo[JoiningLink][2]/2], jointAxis = "0 0 1")
					elif (grandParAxis == 1):
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0]/2, shapeInfo[JoiningLink][1]/2, 0], jointAxis = "1 0 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink  , child = link , type = "revolute", position = [0, shapeInfo[JoiningLink][1]/2, shapeInfo[JoiningLink][2]/2], jointAxis = "0 0 1")
					else:
						if (jointPositionAxis == 0):
							pyrosim.Send_Joint(name = JoiningLink + "_" + link , parent = JoiningLink , child = link , type = "revolute", position = [shapeInfo[JoiningLink][0]/2, 0,  shapeInfo[JoiningLink][2]/2], jointAxis = "1 0 0")
						else:
							pyrosim.Send_Joint(name = JoiningLink + "_" + link, parent = JoiningLink  , child = link , type = "revolute", position = [0, shapeInfo[JoiningLink][1]/2, shapeInfo[JoiningLink][2]/2], jointAxis = "0 1 0")
							
				# Next link
				if (jointPositionAxis == 0):
					self.Send_Shape(shape_choice, name = link + str(i), pos=[length/2,0,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				elif (jointPositionAxis == 1):
					self.Send_Shape(shape_choice, name = link + str(i), pos=[0,width/2,0], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
				else:
					self.Send_Shape(shape_choice, name = link + str(i), pos=[0,0,height/2], size=[length, width, height],mass=1.0, material_name = color_name, rgba=rgba_string )
					
					
				counter += 1
				# flag2 = 1
				
		self.shapeInfo = shapeInfo
		self.total_creature_connections = total_creature_connections
		self.sensorNeuronsList = sensorNeuronsList
		self.shapesAdded = shapesAdded
		
		
		
	def Create_Child_Brain(self):
		pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
		
		counter = 0
		#numSensorNeurons=self.sensorNeurons.count(1)
		numLinks = len(self.shapesAdded)
		for i in range(0,numLinks):
			if (self.sensorNeurons[i] == 1):
				pyrosim.Send_Sensor_Neuron(name = counter , linkName = self.shapesAdded[i])
				counter += 1
				
		child_LinkJointLink = self.total_creature_connections.keys()
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
		
	
					
					
				
				
			
			
			