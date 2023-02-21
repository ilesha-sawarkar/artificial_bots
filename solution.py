import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import time
import constants as c
import math



class SOLUTION:
    def __init__(self, ID):
            self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
            
            self.weights=0
            self.myID= ID
            self.motorNeurons=[]
            self.numSensorNeurons=0
            self.numMotorNeurons=0
            
        
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
        self.numSensorNeurons= c.randSensorsList.count(1)
        self.numMotorNeurons = len(self.motorNeurons)
        
        row = random.randint(0,self.numSensorNeurons-1)
        col = random.randint(0,self.numMotorNeurons-1)
        self.weights[row][col]  =  random.random() * 2 - 1
               
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        x = -30
        y = 10
        z = 0.5
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF(f"body/body{self.myID}.urdf")

        linkLenInfo = {}
        linksAdded = []
        connections = []
        grandConnections = {}
        self.LinkJointLink = []
        locationMatrix = np.zeros((40,40,40,3))

        minX = 0
        minY = 0
        minZ = 0

        maxX = 0
        maxY = 0
        maxZ = 0


        for i in range(0,c.number_of_links):
            # length = random.randint(1,2) * np.random.rand()
            # width = random.randint(1,2) * np.random.rand()
            # height = random.randint(1,2) * np.random.rand()

            length = random.randint(1,2) 
            width = random.randint(1,2) 
            height = random.randint(1,2) 

            if c.randSensorsList[i]==0: #No Sensor
                color_name=c.color_No_Sensor_Link
                rgba_string=c.rgba_No_Sensor_Link 
            else:
                color_name=c.color_Sensor_Link
                rgba_string=c.rgba_Sensor_Link 

           
            if (i == 0):
                pyrosim.Send_Cube(name = "Link" + str(i), pos=[length/2,width/2,height/2] , size=[length,width,height], mass = 1.0, material_name = color_name, rgba=rgba_string )
                minX = 0
                minY = 0
                minZ = 0
                for x in range(length):
                    for y in range(width):
                        for z in range(height):
                            locationMatrix[20+x,20+y,0+z] = 1
                            maxX = 20+x
                            maxY = 20+y
                            maxZ = 0+z
            else:
                pass

            if(i == 0):
                linkLenInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ]]
                linksAdded.append("Link" + str(i))
                b = 1
                g = 0
                tag = "Cyan"
                flag2 = 1
               
            else:
                while(flag2 == 1):
                    jointPositionAxis = random.choice([0, 1, 2])
                    # jointPositionAxis = random.choice([0, 1])
                    # jointPositionAxis = 0
                    linkToJoin = random.choice(linksAdded)

                    if ([jointPositionAxis,linkToJoin] in connections):
                        pass
                    else:
                        linkToJoinPointX = linkLenInfo[linkToJoin][3]
                        linkToJoinPointY = linkLenInfo[linkToJoin][4]
                        linkToJoinPointZ = linkLenInfo[linkToJoin][5]

                        MidPointX = (linkToJoinPointX[0]+linkToJoinPointX[1])/2
                        MidPointY = (linkToJoinPointY[0]+linkToJoinPointY[1])/2
                        MidPointZ = (linkToJoinPointZ[0]+linkToJoinPointZ[1])/2

                        tempLocationMatrix = locationMatrix.copy()
                        positionTaken = np.array([1,1,1])
                        if jointPositionAxis == 0:
                            for x2 in range(length):
                                for y2 in range(width):
                                    for z2 in range(height):

                                      
                                        if (locationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
                                            flag2 = 1
                                            tempLocationMatrix = locationMatrix.copy()

                                            break
                                        else:
                                            flag2 = 0
                                            minX = linkToJoinPointX[1]
                                            maxX = minX + length
                                            minY = MidPointY - width/2
                                            maxY = minY + width
                                            minZ = MidPointZ - height/2
                                            maxZ = minZ + height
                                            tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1

                                      
                        elif jointPositionAxis == 1:
                            for x2 in range(length):
                                for y2 in range(width):
                                    for z2 in range(height):
                                        
                                        if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(y2 + linkToJoinPointY[1]), math.ceil(MidPointZ - height/2 + z2)] == positionTaken).all():
                                            flag2 = 1
                                            tempLocationMatrix = locationMatrix.copy()

                                            break
                                        else:
                                            flag2 = 0
                                            minX = MidPointX - length/2
                                            maxX = minX + length
                                            minY = linkToJoinPointY[1]
                                            maxY = minY + width
                                            minZ = MidPointZ - height/2
                                            maxZ = minZ + height
                                            tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1

                        else:
                            for x2 in range(length):
                                for y2 in range(width):
                                    for z2 in range(height):
                                        
                                        if (locationMatrix[math.ceil(MidPointX - length/2 + x2), math.ceil(MidPointY - width/2 + y2), math.ceil(z2 + linkToJoinPointZ[1])] == positionTaken).all():
                                            flag2 = 1
                                            tempLocationMatrix = locationMatrix.copy()
                                            break
                                        else:
                                            flag2 = 0
                                            minX = MidPointX - length/2
                                            maxX = minX + length
                                            minY = MidPointY - width/2
                                            maxY = minY + width
                                            minZ = linkToJoinPointZ[1]
                                            maxZ = minZ + height
                                            tempLocationMatrix[math.ceil(x2 + linkToJoinPointX[1]), math.ceil(MidPointY - width/2 + y2), math.ceil(MidPointZ - height/2 + z2)] = 1
                
                locationMatrix = tempLocationMatrix.copy()

                                            
                linkLenInfo["Link" + str(i)] = [length, width, height,[minX,maxX],[minY,maxY],[minZ,maxZ]]
                

                linksAdded.append("Link" + str(i))
                connections.append([jointPositionAxis,linkToJoin])  
                grandConnections[linkToJoin+"_"+"Link"+ str(i)] = jointPositionAxis
                # print(grandConnections)
                
                # LinkJointLinkRev = self.LinkJointLink.copy()
                # LinkJointLinkRev = LinkJointLinkRev.reverse()
                # print(LinkJointLinkRev, "reversed")
                for li in reversed(range(len(self.LinkJointLink))) :
                    if ("_"+linkToJoin) in self.LinkJointLink[li]:
                        grandparentLink = self.LinkJointLink[li]
                        grandParAxis = grandConnections[grandparentLink]
                        break
                
                
                if (linkToJoin == "Link0"):
                    if (jointPositionAxis == 0):
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0], linkLenInfo[linkToJoin][1]/2, linkLenInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    elif (jointPositionAxis == 1):
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, linkLenInfo[linkToJoin][1], linkLenInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    else:
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, linkLenInfo[linkToJoin][1]/2, linkLenInfo[linkToJoin][2]], jointAxis = "0 0 1")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    
                elif(grandParAxis == jointPositionAxis):
                    if (jointPositionAxis == 0):
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0],0,0], jointAxis = "1 0 0")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    elif (jointPositionAxis == 1):
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [0,linkLenInfo[linkToJoin][1],0], jointAxis = "0 1 0")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    else:
                        pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0,0,linkLenInfo[linkToJoin][2]], jointAxis = "0 0 1")
                        self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                
                else:
                    if (grandParAxis == 0):
                        if (jointPositionAxis == 1):
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, linkLenInfo[linkToJoin][1]/2, 0], jointAxis = "0 1 0")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                        else:
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, 0, linkLenInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    elif (grandParAxis == 1):
                        if (jointPositionAxis == 0):
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, linkLenInfo[linkToJoin][1]/2, 0], jointAxis = "1 0 0")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                        else:
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, linkLenInfo[linkToJoin][1]/2, linkLenInfo[linkToJoin][2]/2], jointAxis = "0 0 1")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                    else:
                        if (jointPositionAxis == 0):
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin , child = "Link" + str(i) , type = "revolute", position = [linkLenInfo[linkToJoin][0]/2, 0,  linkLenInfo[linkToJoin][2]/2], jointAxis = "1 0 0")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                        else:
                            pyrosim.Send_Joint(name = linkToJoin + "_" + "Link" + str(i) , parent = linkToJoin  , child = "Link" + str(i) , type = "revolute", position = [0, linkLenInfo[linkToJoin][1]/2, linkLenInfo[linkToJoin][2]/2], jointAxis = "0 1 0")
                            self.motorNeurons.append(linkToJoin + "_" + "Link" + str(i))
                        

                




                if (jointPositionAxis == 0):
                    pyrosim.Send_Cube(name = "Link" +str(i), pos=[length/2,0,0] , size=[length,width,height], mass = 1.0, material_name = color_name, rgba=rgba_string)
                elif (jointPositionAxis == 1):
                    pyrosim.Send_Cube(name = "Link" +str(i), pos=[0,width/2,0] , size=[length,width,height], mass = 1.0, material_name = color_name, rgba=rgba_string)
                else:
                    pyrosim.Send_Cube(name = "Link" +str(i), pos=[0,0,height/2] , size=[length,width,height], mass = 1.0, material_name = color_name, rgba=rgba_string)

                self.LinkJointLink.append(linkToJoin + "_" + "Link" + str(i))
                # print(self.LinkJointLink, "straight")
                flag2 = 1

                


        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain/brain{self.myID}.nndf")
        self.numSensorNeurons=c.randSensorsList.count(1)
        self.numMotorNeurons = len(self.motorNeurons)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        print(self.numSensorNeurons,self.numMotorNeurons)
        print("synapse_weights: ", self.weights)
        
        i=0
        for link in c.randSensorsList:
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
        
    

        
            