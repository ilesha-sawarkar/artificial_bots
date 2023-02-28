from world import WORLD
from robot import ROBOT
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):

        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

       
        self.directOrGUI = directOrGUI
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)

        self.world = WORLD(self.physicsClient)
        self.robot = ROBOT(solutionID)
          

    def Run(self):
        for t in range(0,c.simLength):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                time.sleep( 1/6400 )
            # print(t) 
    
    def __del__(self):
        p.disconnect()

    def Get_Fitness(self, solutionID):
        obj = self.world.Get_Position(0)
        self.robot.Get_Fitness(solutionID, obj)
        