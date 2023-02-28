import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy 
import constants as c


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        # self.Prepare_To_Act()

    # def Prepare_To_Act(self):
    #     self.amplitude = c.amplitudeBackLeg

    #     if self.jointName == "Torso_FrontLeg":
    #         self.frequency = c.frequencyBackLeg/2
    #     else:
    #         self.frequency = c.frequencyBackLeg
        
    #     self.offset = c.phaseOffsetBackLeg

    #     self.targetAnglesBackLeg = self.amplitude  * numpy.sin(self.frequency  * numpy.linspace(0, 2*(numpy.pi), c.simLength) + self.offset)

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = self.jointName,
        controlMode = p.POSITION_CONTROL,
        targetPosition = desiredAngle,
        maxForce = c.maxForceBackLeg)

    # def Save_Values(self):
    #     # numpy.save("./data/targetAnglesBackLeg.npy", targetAnglesBackLeg)
    #     # numpy.save("./data/targetAnglesFrontLeg.npy", targetAnglesFrontLeg)
    #     pass