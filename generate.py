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
	#pyrosim.Send_Sphere(name="BowlingBall" , pos=[-3,+3,0.5] , size=[0.5])
	#pyrosim.Send_Cylinder(name='Cyli', pos=[-3,+3,0.5] , size=[1,0.5])
	pyrosim.Send_Sphere(name="Head_circle" , pos=[-3,5,0.5] , size=[0.5], mass=0.2)
	#pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])

	#x=2
	#y=2
	#z=2
	#pyrosim.Send_Cube(name="Box2", pos=[x,y, z] , size=[length, width, height])
	
	pyrosim.End()
	
def Generate_Body():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos=[1.5,0,0.5], size=[1,1,1])
	pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5,0,-0.5])
	
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5], size=[1,1,1])
	
	pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[1,1,1])
	pyrosim.End()
	
	
def Create_Body():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Sphere(name="Head" , pos=[0,0,1.2] , size=[0.3], mass=0.2, material_name="Cyan")
	
	
	
	pyrosim.Send_Cube(name="Upper_Body", pos=[0,0,1], size=[0.5,0.8,0.8], rpy="0 1 0")
	
	
	
	pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[1,1,1], mass=0.5, rpy="0 0 1")
	pyrosim.Send_Joint(name="Torso_UpperBody", parent="Torso", child="Upper_Body", type="fixed", position=[0,0, 0.5], jointAxis= "1 0 0")
	pyrosim.Send_Joint(name="Head_joint", parent="Upper_Body", child="Head", type="spherical", position=[0,0, 0.4], jointAxis= "1 0 0")
	
	
		
	pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0.3,0.5,-0.3], size=[0.2,1,0.2], rpy="0 10")
	pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")
	pyrosim.Send_Joint(name="FrontLeftLeg_FrontLowerLeftLeg", parent="FrontLeftLeg", child="Lower_FrontLeftLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
	pyrosim.Send_Cube(name="Lower_FrontLeftLeg", pos=[0.3,0,-0.8], size=[0.2,0.2,0.8])
	

	pyrosim.Send_Cube(name="FrontRightLeg", pos=[-0.3,0.5,-0.3], size=[0.2,1,0.2])
	pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0,0.5,1], jointAxis= "1 0 0")	
	pyrosim.Send_Joint(name="FrontRightLeg_FrontLowerRightLeg", parent="FrontRightLeg", child="Lower_FrontRightLeg", type="revolute", position=[0,1,0], jointAxis= "1 0 0")
	pyrosim.Send_Cube(name="Lower_FrontRightLeg", pos=[-0.3,0,-0.8], size=[0.2,0.2,0.8])
	
	
		
#	
#	
	pyrosim.Send_Cube(name="BackLeftLeg", pos=[0.3, -0.5,-0.3], size=[0.2,1,0.2])

	pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")
	pyrosim.Send_Joint(name="BackLeftLeg_BackLowerLeftLeg", parent="BackLeftLeg", child="Lower_BackLeftLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
	pyrosim.Send_Cube(name="Lower_BackLeftLeg", pos=[0.3,0,-0.8], size=[0.2,0.2,0.8])

	pyrosim.Send_Cube(name="BackRightLeg", pos=[-0.3, -0.5,-0.3], size=[0.2,1,0.2])
	pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", position=[0,-0.5, 1], jointAxis= "1 0 0")	
	pyrosim.Send_Joint(name="BackRightLeg_BackLowerRightLeg", parent="BackRightLeg", child="Lower_BackRightLeg", type="revolute", position=[0,-1,0], jointAxis= "1 0 0")
	pyrosim.Send_Cube(name="Lower_BackRightLeg", pos=[-0.3,0,-0.8], size=[0.2,0.2,0.8])

#	
#		
	
	
	
	pyrosim.Send_Cube(name="RightLeftLeg", pos=[0.5, 0.3,-0.3], size=[1,0.2,0.2])

	pyrosim.Send_Joint(name="Torso_RightLeftLeg", parent="Torso", child="RightLeftLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
	pyrosim.Send_Joint(name="RightLeftLeg_RightLowerLeftLeg", parent="RightLeftLeg", child="Lower_RightLeftLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
	pyrosim.Send_Cube(name="Lower_RightLeftLeg", pos=[0,0.3,-0.8], size=[0.2,0.2,0.8])
	
	
	
	pyrosim.Send_Cube(name="RightRightLeg", pos=[0.5, -0.3,-0.3], size=[1,0.2,0.2])
	
	pyrosim.Send_Joint(name="Torso_RightRightLeg", parent="Torso", child="RightRightLeg", type="revolute", position=[0.5,0, 1], jointAxis= "0 1 0")
	pyrosim.Send_Cube(name="Lower_RightRightLeg", pos=[0,-0.3,-0.8], size=[0.2,0.2,0.8])
	
	pyrosim.Send_Joint(name="RightRightLeg_RightLowerRightLeg", parent="RightRightLeg", child="Lower_RightRightLeg", type="revolute", position=[1,0,0], jointAxis= "0 1 0")
	
	
	
	pyrosim.Send_Cube(name="LeftRightLeg", pos=[-0.5, 0.3,-0.3], size=[1,0.2,0.2])
	pyrosim.Send_Joint(name="Torso_LeftRightLeg", parent="Torso", child="LeftRightLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
	pyrosim.Send_Cube(name="Lower_LeftRightLeg", pos=[0,0.3,-0.8], size=[0.2,0.2,0.8])
	
	pyrosim.Send_Joint(name="LeftRightLeg_LeftLowerRightLeg", parent="LeftRightLeg", child="Lower_LeftRightLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
	
	pyrosim.Send_Cube(name="LeftLeftLeg", pos=[-0.5, -0.3,-0.3], size=[1,0.2,0.2])
	pyrosim.Send_Joint(name="Torso_LeftLeftLeg", parent="Torso", child="LeftLeftLeg", type="revolute", position=[-0.5,0, 1], jointAxis= "0 1 0")
	pyrosim.Send_Cube(name="Lower_LeftLeftLeg", pos=[0,-0.3,-0.8], size=[0.2,0.2,0.8])
	
	pyrosim.Send_Joint(name="LeftLeftLeg_LeftLowerLeftLeg", parent="LeftLeftLeg", child="Lower_LeftLeftLeg", type="revolute", position=[-1,0,0], jointAxis= "0 1 0")
	
	
		
	pyrosim.End()
		
	
def Create_Brain():
	
	pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
	
	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Head")
	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Upper_Body")
	pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "FrontLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "FrontLeftLeg_FrontLowerLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 5, linkName = "FrontRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontRightLeg_FrontLowerRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "BackLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 8, linkName = "BackLowerLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 9, linkName = "BackRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "BackLowerRightLeg")
	
	pyrosim.Send_Sensor_Neuron(name = 11, linkName = "RightLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "RightLowerLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 13 , linkName = "RightRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 14, linkName = "RightLowerRightLeg")	
	pyrosim.Send_Sensor_Neuron(name = 15, linkName = "LeftRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 16 , linkName = "LeftLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 17, linkName = "LeftLowerRightLeg")
	pyrosim.Send_Sensor_Neuron(name = 18, linkName = "LeftLowerLeftLeg")
	
	
	
	pyrosim.Send_Motor_Neuron( name = 19 , jointName = "Torso_UpperBody")
	pyrosim.Send_Motor_Neuron( name = 20 , jointName = "Head_joint")
	
	pyrosim.Send_Motor_Neuron( name = 21 , jointName = "Torso_FrontLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 22 , jointName = "Lower_FrontLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 23 , jointName = "Torso_FrontRightLeg")
	pyrosim.Send_Motor_Neuron( name = 24 , jointName = "FrontLowerRightLeg")
	
	pyrosim.Send_Motor_Neuron( name = 25, jointName = "Torso_BackLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 26, jointName = "BackLeftLeg_BackLowerLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 27, jointName = "Torso_BackRightLeg")
	pyrosim.Send_Motor_Neuron( name = 28, jointName = "BackLowerRightLeg")
	
	pyrosim.Send_Motor_Neuron( name = 29, jointName = "Torso_RightLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 30, jointName = "RightLeftLeg_RightLowerLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 31, jointName = "Torso_RightRightLeg")
	pyrosim.Send_Motor_Neuron( name = 32, jointName = "RightLowerRightLeg")
	
	pyrosim.Send_Motor_Neuron( name = 33, jointName = "Torso_LeftRightLeg")
	pyrosim.Send_Motor_Neuron( name = 34, jointName = "LeftRightLeg_LeftLowerRightLeg")
	pyrosim.Send_Motor_Neuron( name = 35, jointName = "Torso_LeftLeftLeg")
	pyrosim.Send_Motor_Neuron( name = 36, jointName = "LeftLowerLeftLeg")
	
	for currentRow in range(c.numSensorNeurons):
		for currentColumn in range(c.numMotorNeurons):
			pyrosim.Send_Synapse( 
				sourceNeuronName = currentRow , 
				targetNeuronName = currentColumn+c.numSensorNeurons , 
				weight = random.uniform(-1,1))
	#weight = self.weights[currentRow][currentColumn] )	
					
	pyrosim.End()
	
		
	
	
def Generate_Brain():
	pyrosim.Start_NeuralNetwork("brain.nndf")
	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLeftLeg")
	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontRightLeg")
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