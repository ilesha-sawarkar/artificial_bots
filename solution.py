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
		os.system(f"python3 simulate.py {directOrGui} {self.myID}  2&>1 &")
	
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
		pyrosim.Send_Joint(name="Head_joint", parent="Upper_Body", child="Head", type="revolute", position=[0,0, 0.4], jointAxis= "0 0 1 ")
		
		
		
		pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0.3,0.5,-0.3], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")
		pyrosim.Send_Joint(name="FrontLeftLeg_FrontLowerLeftLeg", parent="FrontLeftLeg", child="FrontLowerLeftLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="FrontLowerLeftLeg", pos=[0.3,0,-0.8], size=[0.2,0.2,0.8])
		
		
		pyrosim.Send_Cube(name="FrontRightLeg", pos=[-0.3,0.5,-0.3], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")	
		pyrosim.Send_Joint(name="FrontRightLeg_FrontLowerRightLeg", parent="FrontRightLeg", child="FrontLowerRightLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="FrontLowerRightLeg", pos=[-0.3,0,-0.8], size=[0.2,0.2,0.8])
		
		
		
	#	
	#	
		pyrosim.Send_Cube(name="BackLeftLeg", pos=[0.3, -0.5,-0.3], size=[0.2,1,0.2])
		
		pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")
		pyrosim.Send_Joint(name="BackLeftLeg_BackLowerLeftLeg", parent="BackLeftLeg", child="BackLowerLeftLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="BackLowerLeftLeg", pos=[0.3,0,-0.8], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Cube(name="BackRightLeg", pos=[-0.3, -0.5,-0.3], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")	
		pyrosim.Send_Joint(name="BackRightLeg_BackLowerRightLeg", parent="BackRightLeg", child="BackLowerRightLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
		pyrosim.Send_Cube(name="BackLowerRightLeg", pos=[-0.3,0,-0.8], size=[0.2,0.2,0.8])
		
	#	
	#		
		
		
		
		pyrosim.Send_Cube(name="RightLeftLeg", pos=[0.5, 0.3,-0.3], size=[1,0.2,0.2])
		
		pyrosim.Send_Joint(name="Torso_RightLeftLeg", parent="Torso", child="RightLeftLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Joint(name="RightLeftLeg_RightLowerLeftLeg", parent="RightLeftLeg", child="RightLowerLeftLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="RightLowerLeftLeg", pos=[0,0.3,-0.8], size=[0.2,0.2,0.8])
		
		
		
		pyrosim.Send_Cube(name="RightRightLeg", pos=[0.5, -0.3,-0.3], size=[1,0.2,0.2])
		
		pyrosim.Send_Joint(name="Torso_RightRightLeg", parent="Torso", child="RightRightLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="RightLowerRightLeg", pos=[0,-0.3,-0.8], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="RightRightLeg_RightLowerRightLeg", parent="RightRightLeg", child="RightLowerRightLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
		
		
		
		pyrosim.Send_Cube(name="LeftRightLeg", pos=[-0.5, 0.3,-0.3], size=[1,0.2,0.2])
		pyrosim.Send_Joint(name="Torso_LeftRightLeg", parent="Torso", child="LeftRightLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="LeftLowerRightLeg", pos=[0,0.3,-0.8], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="LeftRightLeg_LeftLowerRightLeg", parent="LeftRightLeg", child="LeftLowerRightLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
		
		pyrosim.Send_Cube(name="LeftLeftLeg", pos=[-0.5, -0.3,-0.3], size=[1,0.2,0.2])
		pyrosim.Send_Joint(name="Torso_LeftLeftLeg", parent="Torso", child="LeftLeftLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="LeftLowerLeftLeg", pos=[0,-0.3,-0.8], size=[0.2,0.2,0.8])
		
		pyrosim.Send_Joint(name="LeftLeftLeg_LeftLowerLeftLeg", parent="LeftLeftLeg", child="LeftLowerLeftLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")	
		
			
		pyrosim.End()
		

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
		
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLowerLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 3, linkName = "FrontRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "FrontLowerRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "BackLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 6, linkName = "BackLowerLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 7, linkName = "BackRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "BackLowerRightLeg")
		
		pyrosim.Send_Sensor_Neuron(name = 9, linkName = "RightLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "RightLowerLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 11 , linkName = "RightRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 12, linkName = "RightLowerRightLeg")	
		pyrosim.Send_Sensor_Neuron(name = 13, linkName = "LeftRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 14 , linkName = "LeftLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 15, linkName = "LeftLowerRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 16, linkName = "LeftLowerLeftLeg")
		
		
		
		pyrosim.Send_Motor_Neuron( name = 17, jointName = "Head_joint")
		pyrosim.Send_Motor_Neuron( name = 18 , jointName = "Torso_FrontLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 19 , jointName = "FrontLeftLeg_FrontLowerLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 20 , jointName = "Torso_FrontRightLeg")
		pyrosim.Send_Motor_Neuron( name = 21 , jointName = "FrontRightLeg_FrontLowerRightLeg")
		
		pyrosim.Send_Motor_Neuron( name = 22, jointName = "Torso_BackLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 23, jointName = "BackLeftLeg_BackLowerLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 24, jointName = "Torso_BackRightLeg")
		pyrosim.Send_Motor_Neuron( name = 25, jointName = "BackRightLeg_BackLowerRightLeg")
	
		pyrosim.Send_Motor_Neuron( name = 26, jointName = "Torso_RightLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 27, jointName = "RightLeftLeg_RightLowerLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 28, jointName = "Torso_RightRightLeg")
		pyrosim.Send_Motor_Neuron( name = 29, jointName = "RightRightLeg_RightLowerRightLeg")
		
		pyrosim.Send_Motor_Neuron( name = 30, jointName = "Torso_LeftRightLeg")
		pyrosim.Send_Motor_Neuron( name = 31, jointName = "LeftRightLeg_LeftLowerRightLeg")
		pyrosim.Send_Motor_Neuron( name = 32, jointName = "Torso_LeftLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 33, jointName = "LeftLeftLeg_LeftLowerLeftLeg")
	
	
		for currentRow in range(c.numSensorNeurons):
			for currentColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+c.numSensorNeurons , 
					#weight = random.uniform(-1,1),
					weight = self.weights[currentRow][currentColumn] )	
				
		pyrosim.End()

		