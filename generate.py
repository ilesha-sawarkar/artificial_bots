import pyrosim.pyrosim as pyrosim
import random
import constants as c
import os

length =1 
width =1
height=1



def Create_World():
	x=3
	y=1
	z=1
	pyrosim.Start_SDF("world.sdf")
	
	#pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])

	#x=2
	#y=2
	#z=2
	#pyrosim.Send_Cube(name="Box2", pos=[x,y, z] , size=[length, width, height])
	
	pyrosim.End()
	
def Generate_Body():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos=[1.5,0,0.5], size=[1,1,1])
	pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5,0,0])
	
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,0], size=[1,1,1])
	
	pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[1,1,1])
	pyrosim.End()
	
	
def Create_Body():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[1,1,1])
	#pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])
	
	#pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis= " 1 0 0")
	
	
	
	
	#pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
	
	#pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
	
	
	
	pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0,0], size=[0.2,1,0.2])
	
	pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[0,-0.8, 0.5], jointAxis= "1 0 0")
	
	
	
	
	
	
	pyrosim.Send_Cube(name="Lower_LeftLeg", pos=[-0.5,0,0], size=[0.2,0.2,0.8])
	
	pyrosim.Send_Joint(name="Lower_LeftLeg2", parent="LeftLeg", child="Lower_LeftLeg", type="revolute", position=[0,-0.5,-0.5], jointAxis= "1 0 0")
	
	
	pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0], size=[0.2,1,0.2])
	pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0,-0.8, 0.5], jointAxis= "1 0 0")	
	
	pyrosim.Send_Cube(name="Lower_RightLeg", pos=[0.5,0,0], size=[0.2,0.2,0.8])
	
	pyrosim.Send_Joint(name="Lower_RightLeg2", parent="RightLeg", child="Lower_RightLeg", type="revolute", position=[0,-0.5, -0.5], jointAxis= "1 0 0")
	
		
	pyrosim.End()
		
	
def Create_Brain():
	
	pyrosim.Start_NeuralNetwork(f"brain.nndf")
	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "RightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 5, linkName = "BackLowerLeg")
#	pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
	pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Lower_RightLeg")
	pyrosim.Send_Sensor_Neuron(name = 4, linkName = "Lower_LeftLeg")
	
	
#	
#	pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
#	pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
	#pyrosim.Send_Motor_Neuron( name = 11 , jointName = "FrontLeg_FrontLowerLeg")
#	pyrosim.Send_Motor_Neuron( name = 12 , jointName = "RightLeg_RightLowerLeg")
#	pyrosim.Send_Motor_Neuron( name = 13, jointName = "BackLeg_BackLowerLeg")
#	pyrosim.Send_Motor_Neuron( name = 14, jointName = "LeftLeg_LeftLowerLeg")
#	
	pyrosim.Send_Motor_Neuron( name = 5, jointName = "Torso_RightLeg")
	pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
	pyrosim.Send_Motor_Neuron( name = 7, jointName = 
		"Lower_RightLeg2")
	pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Lower_LeftLeg2")
	
	for currentRow in range(5): #c.numSensorNeurons
		for currentColumn in range(4): #c.numMotorNeurons
			pyrosim.Send_Synapse( 
				sourceNeuronName = currentRow , 
				targetNeuronName = currentColumn+5 , 
				weight = random.uniform(-1,1))
				#weight = self.weights[currentRow][currentColumn] )	
			
	pyrosim.End()
	
		
	
	
def Generate_Brain():
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
	
	for sensor in range(0,3):
		for motor in range(3,5):
			pyrosim.Send_Synapse( 
				sourceNeuronName = sensor , 
				targetNeuronName = motor , 
				weight = random.uniform(-1,1))
	
	pyrosim.End()
	
	
	
def Create_Robot():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5], size=[1,1,1])
	pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1.0,0,1.0])
	
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0.5,-0.5], size=[1,1,1])
	
	pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0.5,-0.5], size=[1,1,1])
	pyrosim.End()


Create_World()
Create_Body()
Create_Brain()