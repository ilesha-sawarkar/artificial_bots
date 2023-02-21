#!/usr/bin/env python3
import random

creature_left=0
creature_right=0
creature_front=0
creature_back=0
creature_top=0
creature_bottom=0

def Create_Body(self):
	pyrosim.Start_URDF(f"body/body{self.myID}.urdf")
	self.sensorNeurons=[]
	self.motorNeurons=[]
	self.links_shape =[]
	number_of_links= random.randint(5,8)
	self.sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]
	
	list_shapes=['cube' , 'sphere']
	
	direction=['left','right','front','back','top','bottom']
	
	for i in range(0, number_of_links):
		
		shape_choice=random.choice(list_shapes)
		length=random.randint(1,2)
		width=random.randint(1,2)
		height=random.randint(1,2)
		shape_details=[]
		
		if shape_choice=='sphere':
			#width=width/2
			length=width
			height=width
			width=width/2
		
		shape_size=[length,width,height]
		shape_details=[shape_choice,shape_size]
		
		self.links_shape.append(shape_size,shape_details)
		
		
			
sensorNeurons=[]
motorNeurons=[]
links_shape =[]
number_of_links= random.randint(5,8)
sensorNeurons= [random.randint(0,1) for _ in range (number_of_links)]

list_shapes=['cube' , 'sphere']

direction=['left','right','front','back','top','bottom']

creature_positioning=[]
creature_positioning_1=[]

for i in range(0, number_of_links):
	
	shape_choice=random.choice(list_shapes)
	length=random.randint(1,2)
	width=random.randint(1,2)
	height=random.randint(1,2)
	shape_details=[]
	if shape_choice=='sphere':
		#width=width/2
		length=width
		height=width
		width=width/2
		
	shape_size=[length,width,height]
	shape_details=[shape_choice,shape_size]
	
	
	links_shape.append(shape_details)
	
	
creature_positioning.append('main')	
for i in range(1, number_of_links):
	direction_choice=random.choice(direction)
	#creature_positioning.append('main '+direction_choice)
	string_shape='main '+direction_choice
	if string_shape in creature_positioning:
		
		creature_positioning.append('main '+direction_choice+' '+ direction_choice)
	else:
		creature_positioning.append('main '+direction_choice)
	

print(creature_positioning)
#print(creature_positioning_1)


	

	
	