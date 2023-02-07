#!/usr/bin/env python3
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION :
	def __init__(self, ID):
		
		self.weights=(np.random.rand(c.numSensorNeurons,c.numMotorNeurons))*2 -1   #size=(rows,cols)
		self.myID= ID
		#print(self.weights)
		#exit()
		
	def Evaluate(self,directOrGui ):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system(f"python3 simulate.py {directOrGui} {self.myID} &")
		
		#os.system("python3 simulate.py " + directOrGui + " & ")
		while not os.path.exists(f"data/fitness{self.myID}.txt"):
				time.sleep(0.001)
		fit_file = open(f"data/fitness{self.myID}.txt", "r")
		#fit_file = open(f"data/fitness{self.myID}.txt", "r")
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
		os.system(f"python3 simulate.py {directOrGui} {self.myID} 2&>1 &")
	
	def Wait_For_Simulation_To_End(self):
		while not os.path.exists(f"data/fitness{self.myID}.txt"):
			time.sleep(0.01)
		fit_file = open(f"data/fitness{self.myID}.txt", "r")
		fitness = fit_file.read()
		if fitness == '':
			# print(f"Waiting on {self.myID}")
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
		
		#pyrosim.Send_Cube(name="Box", pos=[1,1, 1] , size=[1, 1, 1])
		
		pyrosim.End()
		
		
		
	def Create_Body(self):
		
		pyrosim.Start_URDF("body.urdf")
				
		pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[1,1,1])
		pyrosim.Send_Sphere(name="Head" , pos=[0,0,1.2] , size=[0.3])
		
		
		
		pyrosim.Send_Cube(name="Upper_Body", pos=[0,0,1], size=[0.5,0.8,0.8])
		
		
		
		
		pyrosim.Send_Joint(name="Torso_UpperBody", parent="Torso", child="Upper_Body", type="fixed", position=[0,0, 0.5], jointAxis= "1 0 0")
		pyrosim.Send_Joint(name="Head_joint", parent="Upper_Body", child="Head", type="spherical", position=[0,0, 0.4], jointAxis= "1 0 0")
		
		
		
		pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0.3,0.5,0], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")
		pyrosim.Send_Joint(name="Lower_FrontLeftLeg2", parent="FrontLeftLeg", child="Lower_FrontLeftLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="Lower_FrontLeftLeg", pos=[0.3,0,-0.5], size=[0.2,0.2,0.8])
		
		
		pyrosim.Send_Cube(name="FrontRightLeg", pos=[-0.3,0.5,0], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")	
		pyrosim.Send_Joint(name="Lower_FrontRightLeg2", parent="FrontRightLeg", child="Lower_FrontRightLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="Lower_FrontRightLeg", pos=[-0.3,0,-0.5], size=[0.2,0.2,0.8])
		
		


		pyrosim.Send_Cube(name="BackLeftLeg", pos=[0.3, -0.5,0], size=[0.2,1,0.2])
		
		pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")
		pyrosim.Send_Joint(name="Lower_BackLeftLeg2", parent="BackLeftLeg", child="Lower_BackLeftLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="Lower_BackLeftLeg", pos=[0.3,0,-0.5], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Cube(name="BackRightLeg", pos=[-0.3, -0.5,0], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")	
		pyrosim.Send_Joint(name="Lower_BackRightLeg2", parent="BackRightLeg", child="Lower_BackRightLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="Lower_BackRightLeg", pos=[-0.3,0,-0.5], size=[0.2,0.2,0.8])
		
	
		
		
		pyrosim.Send_Cube(name="RightLeftLeg", pos=[0.5, 0.3,0], size=[1,0.2,0.2])
		
		pyrosim.Send_Joint(name="Torso_RightLeftLeg", parent="Torso", child="RightLeftLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Joint(name="Lower_RightLeftLeg2", parent="RightLeftLeg", child="Lower_RightLeftLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="Lower_RightLeftLeg", pos=[0,0.3,-0.5], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Cube(name="RightRightLeg", pos=[0.5, -0.3,0], size=[1,0.2,0.2])
		
		pyrosim.Send_Joint(name="Torso_RightRightLeg", parent="Torso", child="RightRightLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="Lower_RightRightLeg", pos=[0,-0.3,-0.5], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="Lower_RightRightLeg2", parent="RightRightLeg", child="Lower_RightRightLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
		
		
		
		pyrosim.Send_Cube(name="LeftRightLeg", pos=[-0.5, 0.3,0], size=[1,0.2,0.2])
		pyrosim.Send_Joint(name="Torso_LeftRightLeg", parent="Torso", child="LeftRightLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="Lower_LeftRightLeg", pos=[0,0.3,-0.5], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="Lower_LeftRightLeg2", parent="LeftRightLeg", child="Lower_LeftRightLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
		
		pyrosim.Send_Cube(name="LeftLeftLeg", pos=[-0.5, -0.3,0], size=[1,0.2,0.2])
		pyrosim.Send_Joint(name="Torso_LeftLeftLeg", parent="Torso", child="LeftLeftLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="Lower_LeftLeftLeg", pos=[0,-0.3,-0.5], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="Lower_LeftLeftLeg2", parent="LeftLeftLeg", child="Lower_LeftLeftLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
		
		
		pyrosim.End()
		
		
	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
		
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Head")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Upper_Body")
		pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "FrontLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "Lower_FrontLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 5, linkName = "FrontRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "Lower_FrontRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "BackLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 8, linkName = "Lower_BackLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 9, linkName = "BackRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "Lower_BackRightLeg")
		
		pyrosim.Send_Sensor_Neuron(name = 11, linkName = "RightLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "Lower_RightLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 13 , linkName = "RightRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 14, linkName = "Lower_RightRightLeg")	
		pyrosim.Send_Sensor_Neuron(name = 15, linkName = "LeftRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 16 , linkName = "LeftLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 17, linkName = "Lower_LeftRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 18, linkName = "Lower_LeftLeftLeg")
		
		
		
		pyrosim.Send_Motor_Neuron( name = 19 , jointName = "Torso_UpperBody")
		pyrosim.Send_Motor_Neuron( name = 20 , jointName = "Head_joint")
		
		pyrosim.Send_Motor_Neuron( name = 21 , jointName = "Torso_FrontLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 22 , jointName = "Lower_FrontLeftLeg2")
		pyrosim.Send_Motor_Neuron( name = 23 , jointName = "Torso_FrontRightLeg")
		pyrosim.Send_Motor_Neuron( name = 24 , jointName = "Lower_FrontRightLeg2")
		
		pyrosim.Send_Motor_Neuron( name = 25, jointName = "Torso_BackLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 26, jointName = "Lower_BackLeftLeg2")
		pyrosim.Send_Motor_Neuron( name = 27, jointName = "Torso_BackRightLeg")
		pyrosim.Send_Motor_Neuron( name = 28, jointName = "Lower_BackRightLeg2")
	
		pyrosim.Send_Motor_Neuron( name = 29, jointName = "Torso_RightLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 30, jointName = "Lower_RightLeftLeg2")
		pyrosim.Send_Motor_Neuron( name = 31, jointName = "Torso_RightRightLeg")
		pyrosim.Send_Motor_Neuron( name = 32, jointName = "Lower_RightRightLeg2")
		
		pyrosim.Send_Motor_Neuron( name = 33, jointName = "Torso_LeftLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 34, jointName = "Lower_LeftLeftLeg2")
		pyrosim.Send_Motor_Neuron( name = 35, jointName = "Torso_LeftRightLeg")
		pyrosim.Send_Motor_Neuron( name = 36, jointName = "Lower_LeftRightLeg2")
		

		
		for currentRow in range(c.numSensorNeurons):
			for currentColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+c.numSensorNeurons , 
					#weight = random.uniform(-1,1),
					weight = self.weights[currentRow][currentColumn] )	
		
		pyrosim.End()

		