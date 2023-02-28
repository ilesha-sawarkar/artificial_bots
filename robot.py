import os
from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
import math
import numpy

class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body"+str(solutionID)+".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)  
        self.Prepare_To_Sense() 
        self.nn = NEURAL_NETWORK("brain"+str(solutionID)+".nndf")
        self.Prepare_To_Act()
        os.system("rm brain"+str(solutionID)+".nndf")
        os.system("rm body"+str(solutionID)+".urdf")
        self.fitnessArray = []
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, t):
        for i in self.sensors:
            self.sensors[i].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                # print(neuronName + " " + jointName + " " + str(desiredAngle))



        # for i in self.motors:
        #     self.motors[i].Set_Value(self.robotId, t)

    def Save_Values(self):
        self.motors.Save_Values()
        self.sensors.Save_Values()
    
    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self, solutionID, obj):
        # stateOfLinkZero = p.getLinkState(self.robotId,0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]
        objectPosition = obj
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # print(basePositionAndOrientation)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        # print(xCoordinateOfLinkZero, "tuplefs")

        position = obj[0]
        objxPosition = position[0]
        objyPosition = position[1]
        objheight = position[2]

        # print("x:", objxPosition)
        # print("y:", objyPosition)


        EuclideanDist = math.dist([objxPosition,objyPosition],[xPosition, yPosition])
        print(EuclideanDist, "dist")

        f = open("tmp"+ str(solutionID)+ ".txt", "w")

        f.write(str(EuclideanDist))
        f.close()
        os.system("mv tmp"+ str(solutionID)+ ".txt fitness" + str(solutionID) + ".txt")
        # self.fitnessArray.append(EuclideanDist)
        # fitnessnumpy = numpy.array(self.fitnessArray)
        # numpy.save("./data/fitness"+str(solutionID)+".npy", fitnessnumpy)

        exit()


   
      
