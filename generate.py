import pyrosim.pyrosim as pyrosim

length =1 
width =1
height=1

def Create_World():
	x=0
	y=0
	z=0.5
	pyrosim.Start_SDF("world.sdf")
	
	
	pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])

	#x=2
	#y=2
	#z=2
	#pyrosim.Send_Cube(name="Box2", pos=[x,y, z] , size=[length, width, height])
	
	pyrosim.End()
	
def Create_Robot():
	x=2
	y=2
	z=0.5
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos=[x,y, z] , size=[length, width, height])
	pyrosim.Send_Cube(name="Leg", pos=[1,0,1.5] , size=[length, width, height])
	pyrosim.End()
	


Create_World()
Create_Robot()