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
		self.creature_length_pos=0
		self.creature_width_pos=0
		self.creature_height_pos=0
		self.creature_height_pos_left=0
		self.creature_height_pos_right=0
		self.creature_length_neg=0
		self.creature_width_neg=0
		self.creature_height_neg=0
		
		
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
		self.numSensorNeurons=self.sensorNeurons.count(1)
		self.numMotorNeurons = len(self.motorNeurons)
		
		row = random.randint(0,self.numSensorNeurons-1)
		col = random.randint(0,self.numMotorNeurons-1)
		self.weights[row][col]  =  random.random() * 2 - 1
	
	def Create_World(self):
		
		pyrosim.Start_SDF("world.sdf")
		
		#pyrosim.Send_Capsule(name="Head_circle" , pos=[3,5,0.5] , size=[0.02,0.5,1], mass=1.0, material_name='Red', rgba="1.0 0.0 1.0 1.0")
		
		pyrosim.End()
		
		
	def Send_Cube_Direction(self, shape_choice,  length, width,height, cube_direction, placement_position):
		
		
		#creature_width=total_creature_size[1]
		#creature_height=total_creature_size[2]
		print(cube_direction, ' ', placement_position)
		z_direction=['up']
		y_direction=['left','right']
		x_direction=['left','right']
		
		if shape_choice=='sphere':
			#width=width/2
			length=width
			height=width
			width=width/2
			
		
		if cube_direction=='x':
			
			y_choice=random.choice(x_direction)
			
			if placement_position=='positive':
				if y_choice=='left':
					cube_position=[length/2, 0, height/2]
					joint_position=[length/1,self.creature_width_pos/2 , self.creature_height_pos]
					self.creature_length_pos=length
					self.creature_height_pos_left=height
					self.creature_width_neg=width
					joint_direction='1 0 0'
				elif y_choice =='right':
					cube_position=[length/2, 0, height/2]
					joint_position=[length,-self.creature_width_neg/2 , self.creature_height_pos]
					self.creature_length_pos=length
					self.creature_height_pos_right=height
					self.creature_width_pos=width
					joint_direction='1 0 0'
				
			elif placement_position=='negative':
				if y_choice=='left':
					cube_position=[length/-2, 0, height/2]
					joint_position=[-length,self.creature_width_pos/2 , self.creature_height_pos]
					self.creature_length_neg=length
					self.creature_height_pos_left=height
					self.creature_width_neg=width
					joint_direction='1 0 0'
				elif y_choice =='right':
					cube_position=[length/-2, 0, height/2]
					joint_position=[-length, -self.creature_width_neg/2,self.creature_height_pos]
					self.creature_length_neg=length
					self.creature_height_pos_right=height
					self.creature_width_pos=width
					joint_direction='1 0 0'
				
			
			
		elif cube_direction=='y':
			x_choice=random.choice(x_direction)
			if placement_position=='positive':
				if x_choice== 'left':
					cube_position=[0, self.creature_width_pos/1,height/2]
					joint_position=[self.creature_length_pos, width/1,  self.creature_height_pos/2]
					self.creature_length_pos=length
					self.creature_width_pos=width
					joint_direction='0 1 0'
				elif x_choice =='right':
					cube_position=[0, self.creature_width_pos/1,height/2]
					joint_position=[self.creature_length_pos, width/1,  self.creature_height_pos]
					self.creature_length_pos=length
					self.creature_width_pos=width
					joint_direction='0 1 0'
					
			elif placement_position=='negative':
				if x_choice== 'left':
					cube_position=[0, self.creature_width_pos/-1, height/2]
					joint_position=[self.creature_length_neg, width/-1,  self.creature_height_pos]
					self.creature_length_neg=length
					self.creature_width_neg=width
					joint_direction='0 1 0'
				elif x_choice == 'right':
					cube_position=[0, self.creature_width_pos/1,height/2]
					joint_position=[self.creature_length_neg, width/-1,  self.creature_height_pos]
					self.creature_length_neg=length
					self.creature_width_neg=width
					joint_direction='0 1 0'
			
			
		elif cube_direction=='z':
			if placement_position=='positive':
				cube_position=[0, 0, height/1.8]
				joint_position=[self.creature_length_pos,self.creature_width_pos,height/1]
				self.creature_height_pos=height
				joint_direction='1 0 0'
			elif placement_position=='negative':
				cube_position=[0, 0, height/-1.8]
				joint_position=[self.creature_length_neg,self.creature_width_neg/1.8,  height/-1]
				self.creature_height_neg=height
				joint_direction='0 0 1'
			
		return cube_position, joint_position, joint_direction
		
	
	def Send_Shape(self, shape, name, position, size, mass, color_name, rgba_string):
		print(shape)
		if shape=='sphere':
			radius=[size[1]/2] #initializing the random assigned width as radius length
			
			print("Sphere :",radius)
			pyrosim.Send_Sphere(name=name , pos= position, size=radius, mass=mass, material_name=color_name, rgba=rgba_string)
		elif shape=='cube':
			pyrosim.Send_Cube(name=name , pos= position, size=size, mass=mass, material_name=color_name, rgba=rgba_string)
#		else:
#			pyrosim.Send_Capsule(name=name , pos= position, size=size, mass=mass, material_name=color_name, rgba=rgba_string)
			
	
	
	
	def Create_Body(self):
		pyrosim.Start_URDF(f"body/body{self.myID}.urdf")
		self.sensorNeurons=[]
		self.motorNeurons=[]
				
		length=random.randint(1,2)
		width=random.randint(1,2)
		height=random.randint(1,2)
		list_shapes=['cube' , 'sphere']
		block_direction=['x','z'] #'z',y', , 'negative', 'positive'
		relative_position=['positive','negative']


		shape_choice=random.choice(list_shapes)
		cube_direction= random.choice(block_direction)
		
		placement_position = random.choice(relative_position)
		
		number_of_links= random.randint(5,8)#c.maxLinks)
		
		
		self.sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]
		print(self.sensorNeurons)
		
		print('Creature with total shapes : ', number_of_links)
		if shape_choice =='sphere':
			width=width
		
		cube_position, joint_position, joint_direction =self.Send_Cube_Direction( shape_choice, length, width, height, cube_direction, placement_position)
		
		if self.sensorNeurons[0]==0: #No Sensor
			print(shape_choice)
			
			self.Send_Shape(shape_choice, name="Link0", position=cube_position, size=[length, width, height],mass=1.0, color_name=c.color_No_Sensor_Link, rgba_string=c.rgba_No_Sensor_Link )
		else:
			self.Send_Shape(shape_choice, name="Link0", position=cube_position, size=[length, width, height],mass=1.0, color_name=c.color_Sensor_Link, rgba_string=c.rgba_Sensor_Link )
			#self.creature_height_pos=height
		
			
		pyrosim.Send_Joint(name=f"Link0_Link1", parent="Link0", child="Link1", type="revolute", position=joint_position, jointAxis= joint_direction)
		
		self.motorNeurons.append("Link0_Link1")
		
		total_creature_size= [length, width, height]
		
		
		for i in range(1,number_of_links):
			length=random.randint(1,3)
			width=random.randint(1,2)
			height=random.randint(1,2)
			shape_choice=random.choice(list_shapes)
			cube_direction= random.choice(block_direction)
			placement_position = random.choice(relative_position)
			
			parent_name="Link"+str(i)
			child_name="Link"+str(i+1)
			print(child_name,' : ', length, width, height)
			
			
				
			print(shape_choice)
			
			if self.sensorNeurons[i]==0: #No Sensor
				#pos=[length, width, height]
				cube_position, joint_position, joint_direction =self.Send_Cube_Direction( shape_choice,length, width, height, cube_direction, placement_position)
				
				self.Send_Shape(shape_choice, name=parent_name, position=cube_position, size=[length, width, height],mass=1.0, color_name=c.color_No_Sensor_Link, rgba_string=c.rgba_No_Sensor_Link )
				
			else:
				#pos=[length, width, height]
				cube_position, joint_position, joint_direction =self.Send_Cube_Direction( shape_choice, length, width, height, cube_direction, placement_position)
				
				self.Send_Shape(shape_choice, name=parent_name, position=cube_position, size=[length, width, height],mass=1.0, color_name=c.color_Sensor_Link, rgba_string=c.rgba_Sensor_Link )
				
			if i<number_of_links-1:
				joint_name= "Link"+str(i)+'_'+"Link"+str(i+1)
				
				
				
				pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=child_name, type="revolute", position=joint_position, jointAxis= joint_direction)
				self.motorNeurons.append(joint_name)
		
				
			
				
		print('MotorNeurons',self.motorNeurons)
								
					
		
		
		
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

		