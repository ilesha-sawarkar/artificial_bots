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
	pyrosim.Send_Capsule(name="Head_circle" , pos=[0.5,5,0.5] , size=[], mass=1.0, material_name='Red', rgba="1.0 0.0 1.0 1.0")
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
	y_orientation=0
	shape_length=0
	number_of_links= random.randint(3, 10)
	
	pyrosim.Send_Sphere(name="Head" , pos=[0.5,0,0.5] , size=[0.02,0.5,0.2], mass=1.0, material_name='Red', rgba="1.0 0.0 1.0 1.0")
	#	pyrosim.Send_Cube(name='Torso' , pos=[0,0,0.5], size=[1,1,1])
#	pyrosim.Send_Cube(name='Cube1', pos=[0,0.5,0.5] , size=[1,2,1], mass=1.0, material_name='Red', rgba="0.0 0.0 1.0 1.0")
#	pyrosim.Send_Joint(name='Torso_Cube1', parent='Torso', child='Cube1', type="revolute", position=[0,1,0], jointAxis= "0 1 0")
	
#	for i in range(0,number_of_links):
#		length=random.randint(1,2)
#		width=random.randint(1,2)
#		height=random.randint(1,2)
#		shape_name="Link"+str(i)
#		print(shape_name,' : ', length, width, height)
#		#list_shapes=['cube', 'sphere']
#		#shape_choice=random.choice(list_shapes)
#		#print(shape_choice)
#		
#		
#		
#		if i==0:
#			#print('Initial: ', length, width, height)
#			print(shape_name,' pos : ',0,0,height/2)
#			pyrosim.Send_Cube(name=shape_name, pos=[0,0,height/2], size=[length, width, height])
#			old_width=width/2
#		else:
#				#if shape_choice=='cube':
#				#print(length, width, height)
#			print(shape_name,' pos : ',0,old_width,0.5)
#			pyrosim.Send_Cube(name=shape_name , pos=[0,old_width,0] , size=[length, width, height], mass=1.0, material_name='Red', rgba="1.0 1.0 0.0 1.0")
#				#			elif shape_choice=='sphere':
#
#			joint_name="Link"+str(i-1)+'_'+"Link"+str(i)
#			parent_name="Link"+str(i-1)
#			child_name="Link"+str(i)
#			
#			if i==1:
#				print(joint_name,' Joint: ', 0,old_width, 0)
#				pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=child_name, type="revolute", position=[0,old_width,0], jointAxis= "0 1 0")
#				old_width=old_width+width
#			else:
#				print(joint_name,' Joint: ', 0,shape_length, 0)
#				
#				pyrosim.Send_Joint(name=joint_name, parent=parent_name, child=child_name, type="revolute", position=[0,shape_length, 0.5], jointAxis= "0 1 0")
#				old_width=old_width+width
#			
			
		
		
	
	
	
		
	pyrosim.End()
		
	
def Create_Brain():
	
	pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
#	
#	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
#	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Head")
#	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Upper_Body")
#	pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "FrontLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "FrontLeftLeg_FrontLowerLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 5, linkName = "FrontRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontRightLeg_FrontLowerRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "BackLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 8, linkName = "BackLowerLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 9, linkName = "BackRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "BackLowerRightLeg")
#	
#	pyrosim.Send_Sensor_Neuron(name = 11, linkName = "RightLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "RightLowerLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 13 , linkName = "RightRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 14, linkName = "RightLowerRightLeg")	
#	pyrosim.Send_Sensor_Neuron(name = 15, linkName = "LeftRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 16 , linkName = "LeftLeftLeg")
#	pyrosim.Send_Sensor_Neuron(name = 17, linkName = "LeftLowerRightLeg")
#	pyrosim.Send_Sensor_Neuron(name = 18, linkName = "LeftLowerLeftLeg")
#	
#	
#	
#	pyrosim.Send_Motor_Neuron( name = 19 , jointName = "Torso_UpperBody")
#	pyrosim.Send_Motor_Neuron( name = 20 , jointName = "Head_joint")
#	
#	pyrosim.Send_Motor_Neuron( name = 21 , jointName = "Torso_FrontLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 22 , jointName = "Lower_FrontLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 23 , jointName = "Torso_FrontRightLeg")
#	pyrosim.Send_Motor_Neuron( name = 24 , jointName = "FrontLowerRightLeg")
#	
#	pyrosim.Send_Motor_Neuron( name = 25, jointName = "Torso_BackLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 26, jointName = "BackLeftLeg_BackLowerLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 27, jointName = "Torso_BackRightLeg")
#	pyrosim.Send_Motor_Neuron( name = 28, jointName = "BackLowerRightLeg")
#	
#	pyrosim.Send_Motor_Neuron( name = 29, jointName = "Torso_RightLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 30, jointName = "RightLeftLeg_RightLowerLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 31, jointName = "Torso_RightRightLeg")
#	pyrosim.Send_Motor_Neuron( name = 32, jointName = "RightLowerRightLeg")
#	
#	pyrosim.Send_Motor_Neuron( name = 33, jointName = "Torso_LeftRightLeg")
#	pyrosim.Send_Motor_Neuron( name = 34, jointName = "LeftRightLeg_LeftLowerRightLeg")
#	pyrosim.Send_Motor_Neuron( name = 35, jointName = "Torso_LeftLeftLeg")
#	pyrosim.Send_Motor_Neuron( name = 36, jointName = "LeftLowerLeftLeg")
#	
#	for currentRow in range(c.numSensorNeurons):
#		for currentColumn in range(c.numMotorNeurons):
#			pyrosim.Send_Synapse( 
#				sourceNeuronName = currentRow , 
#				targetNeuronName = currentColumn+c.numSensorNeurons , 
#				weight = random.uniform(-1,1))
#	#weight = self.weights[currentRow][currentColumn] )	
					
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
#Create_Brain()