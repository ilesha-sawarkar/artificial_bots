import pyrosim.pyrosim as pyrosim



pyrosim.Start_SDF("world.sdf")
x=0
y=0
z=1
length =1 
width =1
height=1

pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])

	#x=2
	#y=2
	#z=2
#pyrosim.Send_Cube(name="Box2", pos=[x,y, z] , size=[length, width, height])

pyrosim.End()
