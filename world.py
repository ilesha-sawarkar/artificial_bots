import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim

class WORLD:
    def __init__(self, physicsClient):
        self.physicsClient = physicsClient
        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")

    def Get_Position(self, obj):
        posAndOrientation = p.getBasePositionAndOrientation(self.objects[obj])
        return(posAndOrientation)
