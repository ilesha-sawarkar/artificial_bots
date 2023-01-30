#!/usr/bin/env python3
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os

class SOLUTION :
	def __init__(self):
		
		self.weights=(np.random.rand(3,2))*2 -1   #size=(rows,cols)
		#print(self.weights)
		#exit()
		
	def Evaluate(self,directOrGui ):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system("python3 simulate.py " + directOrGui)
		fit_file = open("data/fitness.txt", "r")
		fitness = fit_file.read()
		self.fitness = float(fitness)	
	
		
	def Mutate(self):
		
		row = random.randint(0,2)
		col = random.randint(0,1)
		self.weights[row][col]  =  random.random() * 2 - 1
	
	def Create_World(self):
		
		pyrosim.Start_SDF("world.sdf")
		
		pyrosim.Send_Cube(name="Box", pos=[1,1, 1] , size=[1, 1, 1])
		
		pyrosim.End()
		
	def Create_Body(self):
		pyrosim.Start_URDF("body.urdf")
		pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5], size=[1,1,1])
		pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1.0,0,1.0])
		
		pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5], size=[1,1,1])
		
		pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
		pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[1,1,1])
		pyrosim.End()
		
		
	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain.nndf")
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
		pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
		pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = 1.0 )
		pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 1.0 )
		# add more synapses and weights
		pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4, weight = 1.0 )
		pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )
		pyrosim.Send_Synapse( sourceNeuronName = 0, targetNeuronName = 4 , weight = 1.0 )
		
		for currentRow in range(3):
			for currentColumn in range(2):
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+3 , 
					#weight = random.uniform(-1,1),
					weight = self.weights[currentRow][currentColumn] )				
				
		pyrosim.End()

		
		
		