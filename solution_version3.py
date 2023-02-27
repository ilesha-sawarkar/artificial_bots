import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import time
import constants as c
import pybullet as p
import math
from shape import SHAPE



class SOLUTION:
    def __init__(self, ID):
            self.number_of_links=0
            self.weights=0
            self.myID= ID
            self.motorNeurons=[]
            self.numSensorNeurons=0
            self.numMotorNeurons=0
            #self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
            self.sensorNeuronsLinkNames=[]
            self.sensorNeurons_List=[]
            self.links=[]
            self.LinkDict= {}
            self.root = None   
            
    def Send_Shape(self, shape, name, pos, size, mass, material_name , rgba):
        print(shape)
        if shape=='sphere':
            radius=[size[1]/2] #initializing the random assigned width as radius length
            print("Sphere :",radius)
            pyrosim.Send_Sphere(name=name , pos= pos, size=radius, mass=mass, material_name=material_name, rgba=rgba)
        elif shape=='cube':
            pyrosim.Send_Cube(name=name , pos= pos, size=size, mass=mass, material_name=material_name, rgba=rgba)
            
    
    def Evaluate(self,directOrGui ):
        self.Create_World()
        self.Create_Brain()
        self.Create_Body()
        
        os.system(f"python3 simulate.py {directOrGui} {self.myID} &")
        
        
        while not os.path.exists(f"data/fitness{self.myID}.txt"):
                time.sleep(0.001)
        fit_file = open(f"data/fitness{self.myID}.txt", "r")
        
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
        os.system(f"python3 simulate.py {directOrGui} {self.myID}   &")
        
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"data/fitness{self.myID}.txt"):
            time.sleep(0.01)
        fit_file = open(f"data/fitness{self.myID}.txt", "r")
        fitness = fit_file.read()
        if fitness == '':
            
            time.sleep(0.1)
            fitness = fit_file.read()
        self.fitness = float(fitness)
        print('Fitness: ', self.fitness)
        fit_file.close()
        os.system(f"rm data/fitness{self.myID}.txt")
        
        
    def Mutate(self):
        self.numSensorNeurons= c.numSensorNeurons.count(1)
        self.numMotorNeurons = len(self.motorNeurons)
        
        row = random.randint(0,self.numSensorNeurons-1)
        col = random.randint(0,self.numMotorNeurons-1)
        self.weights[row][col]  =  random.random() * 2 - 1
               
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        x = -10
        y = 5
        z = 0.5
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.End()
        
        
        

    def create_root_shape(self, root_shape=None, shape_choice=None, color_name=None, rgba= None):
            if root_shape == None:
                    root_shape = SHAPE(0)
            position = root_shape.dimensions * np.array([0, 0, 0.5])
            position[2] += 5
            Send_Shape(self, shape, name, pos, size, mass, material_name , rgba)
            Shape(self, shape= shape_choice, name=root_shape.ID, pos= position, size=root_shape.dimensions, mass=1.0, material_name=color_name , rgba= rgba)
            self.links.append(root_shape)
            return root_shape
    
    def create_root_joint(self, root_shape):
            position = root_shape.dimensions * np.array([0, 0.5, 0.5])
            position[2] += 5
            pyrosim.Send_Joint(name = f"Link0_Link1",
                    parent= f"Link0" , 
                    child = f"Link1" , 
                    type = "revolute", 
                    position = position,
                    jointAxis = "1 0 0")
            self.motorNeurons.append(f"Link0_Link1")
        
    def create_first_relative_joint(self, link1=None, shape_choice=None, color_name=None, rgba= None):
            if link1 == None:
                    link1 = SHAPE(1)
            position = link1.dimensions * np.array([0, 0.5, 0])
            Send_Shape(self, shape= shape_choice, name=link1.ID, pos= position, size=link1.dimensions, mass=1.0, material_name=color_name , rgba= rgba)
            self.links.append(link1)
            return link1
    
    def record_sensor_neurons(self, list_sensors):
            for link in list_sensors:
                    if link.isSensor:
                            self.sensorNeurons.append(link.ID)
            for link in list_sensors:
                    self.linkDict[link.ID]= link
                    self.record_sensor_neurons(link.children)
                
                
    def Create_Body(self):
            pyrosim.Start_URDF(f"body/body{self.myID}.urdf")
            self.number_of_links= random.randint(3,c.maxLinks)
            self.sensorNeurons_List= [random.randint(0,1) for _ in range (self.number_of_links)]
            print(self.sensorNeurons_List)
        
            shapes=['cube', 'sphere']
            for i in range(0,self.number_of_links):
                shape_choice=random.choice(shapes)
                if self.sensorNeurons_List[i]==0: #No Sensor
                        color_name=c.color_No_Sensor_Link
                        rgba_string=c.rgba_No_Sensor_Link 
                else:
                    color_name=c.color_Sensor_Link
                    rgba_string=c.rgba_Sensor_Link 
                    
                    
                    
                if len(self.links)==0:
                        
                        root_shape = self.create_root_shape(shape_choice=shape_choice, color_name=color_name, rgba= rgba_string )
                        self.create_root_joint(root_shape)
                        parent = self.create_first_relative_joint(shape_choice=shape_choice, color_name=color_name, rgba= rgba_string)
                        self.links.append(parent)
                        for i in range(2, self.number_of_links):
                                child = SHAPE(str(i), parent, "right")
                                child.create(3/self.number_of_links)
                                self.motorNeurons.append(child.jointID)
                                self.links.append(child)
                                parent = child
                        self.record_sensor_neurons(self.links)
                        # print("sensor names:", self.sensorNeurons)
                        print("link names:", list(self.linkDict.keys()))
                else:
                        self.linkNames = list(self.linkDict.keys())
                        self.linkNames.remove("Link0")
                        self.create_root_shape(self.linkDict["Link0"])
                        self.create_root_joint(self.linkDict["Link0"])
                        self.linkNames.remove("Link1")
                        self.create_first_relative_joint(link1 =self.linkDict["Link1"],shape_choice=shape_choice, color_name=color_name, rgba= rgba_string)
                        for linkName in self.linkNames:
                                # print("Recreating", self.linkDict[linkName].ID)
                                self.linkDict[linkName].create(-1, first_pass=False)
                        
            pyrosim.End()
        
        

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain/brain{self.myID}.nndf")
        self.numSensorNeurons=self.sensorNeurons.count(1)
        self.numMotorNeurons = len(self.motorNeurons)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        print(self.numSensorNeurons,self.numMotorNeurons)
        print("synapse_weights: ", self.weights)
        
        i=0
        for link in self.sensorNeurons:
            if link==1:
                pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link"+str(i))
                i+=1
                
        print(self.motorNeurons)
        for joint in self.motorNeurons:
                pyrosim.Send_Motor_Neuron( name = i , jointName = joint)
                i+=1
            
            
        for currentRow in range(0,self.numSensorNeurons):
            for currentColumn in range(0, self.numMotorNeurons):
                
                pyrosim.Send_Synapse( 
                    sourceNeuronName = currentRow , 
                    targetNeuronName = currentColumn+ self.numSensorNeurons , 
                    weight = self.weights[currentRow][currentColumn] )	
                
        pyrosim.End()
        
    

        
            