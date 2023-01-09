import pyrosim.pyrosim as pyrosim



pyrosim.Start_SDF("boxes.sdf")
x=0
y=0
z=1
length =1 
width =1
height=1

for i in range(0,5):
	
	for j in range(0,5):
		for k in range(0,10):
			pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])
			z=z+1
			length= length*90/100
			width= width*90/100
			height= height*90/100
		y=y+1
		z=1
		length = 1
		width= 1
		height=1
		
	y=0
	x=x+1
			

	#x=2
	#y=2
	#z=2
#pyrosim.Send_Cube(name="Box2", pos=[x,y, z] , size=[length, width, height])

pyrosim.End()
