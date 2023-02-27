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
		
		pyrosim.Send_Cube(name="Box", pos=[5,5, 1] , size=[1, 1, 1])
		
		pyrosim.End()
		
	def Create_Body(self):
		pyrosim.Start_URDF(f"body/body{self.myID}.urdf")
		pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[1,1,1])
		pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0], size=[0.2,1,0.2])
		pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0,-0.5,1.0], jointAxis= "1 0 0")
		
		pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
		
		pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
		
		
		
		pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0], size=[1,0.2,0.2])
		
		pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5,0,1], jointAxis= "0 1 0")
		pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
		pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
		
		
		
		
		
		pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])
		
		pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis= " 1 0 0")
		
		
		
		
		pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
		
		pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
		
		
		pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0], size=[1,0.2,0.2])
		pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5,0,1], jointAxis= "0 1 0")
		
		pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
		
		pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
		
		pyrosim.End()
		
		
	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain/brain{self.myID}.nndf")
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
		pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
		pyrosim.Send_Sensor_Neuron(name = 5, linkName = "BackLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 8, linkName = "RightLowerLeg")
		
		

		pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
		pyrosim.Send_Motor_Neuron( name = 11 , jointName = "FrontLeg_FrontLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 12 , jointName = "RightLeg_RightLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 13, jointName = "BackLeg_BackLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 14, jointName = "LeftLeg_LeftLowerLeg")

		pyrosim.Send_Motor_Neuron( name = 15, jointName = "Torso_RightLeg")
		pyrosim.Send_Motor_Neuron( name = 16 , jointName = "Torso_LeftLeg")

		
		for currentRow in range(c.numSensorNeurons):
			for currentColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse( 
					sourceNeuronName = currentRow , 
					targetNeuronName = currentColumn+c.numSensorNeurons , 
					#weight = random.uniform(-1,1),
					weight = self.weights[currentRow][currentColumn] )	
		
		pyrosim.End()

		
		