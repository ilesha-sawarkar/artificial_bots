#!/usr/bin/env python3
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION :
	def __init__(self, ID):
		
		self.weights=0
		self.myID= ID
		self.sensorNeurons=[]
		self.motorNeurons=[]
		self.numSensorNeurons = 0
		
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
		os.system(f"python3 simulate.py {directOrGui} {self.myID}    &")
	
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
		
		row = random.randint(0,c.numSensorNeurons-1)
		col = random.randint(0,c.numMotorNeurons-1)
		self.weights[row][col]  =  random.random() * 2 - 1
	
	def Create_World(self):
		
		pyrosim.Start_SDF("world.sdf")
		
		pyrosim.Send_Capsule(name="Head_circle" , pos=[3,5,0.5] , size=[0.02,0.5,1], mass=1.0, material_name='Red', rgba="1.0 0.0 1.0 1.0")
		
		pyrosim.End()
		
		
	
	def Send_Shape(self, shape, name, position, size, mass, color_name, rgba_string):
		print(shape)
		if shape=='sphere':
			radius=[size[0]/2]
			print("Sphere :",radius)
			pyrosim.Send_Sphere(name=name , pos= position, size=radius, mass=mass, material_name=color_name, rgba=rgba_string)
		elif shape=='cube':
			pyrosim.Send_Cube(name=name , pos= position, size=size, mass=mass, material_name=color_name, rgba=rgba_string)
#		else:
#			pyrosim.Send_Capsule(name=name , pos= position, size=size, mass=mass, material_name=color_name, rgba=rgba_string)
			
	
	
	
	def Create_Body(self):
		pyrosim.Start_URDF("body.urdf")
				
		length=random.randint(1,2)
		width=random.randint(1,2)
		height=random.randint(1,2)
		list_shapes=['cube', 'sphere']
		shape_choice=random.choice(list_shapes)
		
		snake_length=0
		number_of_links= random.randint(4,5)
		
		self.sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]
		print(self.sensorNeurons)
		
		print('Snake with links : ', number_of_links)
		
		shape_name="Link"+str(0)
		
		if self.sensorNeurons[0]==0: #No Sensor
			self.Send_Shape('cube', name=shape_name, position=[0,0,height/2], size=[length, width, height],mass=1.0, color_name=c.color_No_Sensor_Link, rgba_string=c.rgba_No_Sensor_Link )
		else:
			self.Send_Shape('cube', name=shape_name, position=[0,0,height/2], size=[length, width, height],mass=1.0, color_name=c.color_Sensor_Link, rgba_string=c.rgba_Sensor_Link )
			
		
		old_width=width
		for i in range(1,number_of_links):
			length=random.randint(1,3)
			width=random.randint(1,2)
			height=random.randint(1,2)
			shape_choice=random.choice(list_shapes)
			
			
			joint_name= "Link"+str(i-1)+'_'+"Link"+str(i)
			parent_name="Link"+str(i-1)
			child_name="Link"+str(i)
			print(child_name,' : ', length, width, height)
			print('Joint pos:', joint_name,0,old_width,0)
			
			if i==1:
				pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=child_name, type="revolute", position=[0,old_width/-2,0.5], jointAxis= "0 1 0")
			else:
				pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=child_name, type="revolute", position=[0,width/-1,0.5], jointAxis= "0 1 0")
			self.motorNeurons.append(joint_name)
				
			
			if self.sensorNeurons[i]==0: #No Sensor
				self.Send_Shape(shape_choice, name=child_name, position=[0,width/-2,height/2], size=[length, width, height],mass=1.0, color_name=c.color_No_Sensor_Link, rgba_string=c.rgba_No_Sensor_Link )
			else:
				self.Send_Shape(shape_choice, name=child_name, position=[0,width/-2,height/2], size=[length, width, height],mass=1.0, color_name=c.color_Sensor_Link, rgba_string=c.rgba_Sensor_Link )
				
			old_width=width+old_width
				
					
								
					
		
		
		
		pyrosim.End()
		

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
		self.numSensorNeurons=self.sensorNeurons.count(1)
		self.numMotorNeurons = len(self.motorNeurons)
		self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
		print(self.numSensorNeurons,self.numMotorNeurons)
		print("synapse_weights: ", self.weights)
						
#		i=0
#		for link in self.sensorNeurons:
#			pyrosim.Send_Sensor_Neuron(name = i, linkName = str(link))
#			i+=1
#		for joint in self.motorNeurons:
#			pyrosim.Send_Motor_Neuron( name = i , jointName = str(joint))
#			i+=1
#					
		
	
		for currentRow in range(self.numSensorNeurons):
			for currentColumn in range(self.numMotorNeurons):
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+ self.numSensorNeurons , 
					#weight = random.uniform(-1,1),
					weight = self.weights[currentRow][currentColumn] )	
				#print(self.weights)
				#print(self.weights[currentRow][currentColumn] )
		pyrosim.End()

		