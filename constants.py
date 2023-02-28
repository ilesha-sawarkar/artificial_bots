import numpy 
import random

gravity = -9.8

numpyseed = 54
randomseed = 59876
numpy.random.seed(numpyseed)
random.seed(randomseed)

simLength = 20000

amplitudeBackLeg = numpy.pi/4
frequencyBackLeg = 10
phaseOffsetBackLeg = 0

# phaseOffsetBackLeg = numpy.pi/7

maxForceBackLeg = 70

amplitudeFrontLeg = numpy.pi/3
frequencyFrontLeg = 10
phaseOffsetFrontLeg = 0

maxForceFrontLeg = 70

numberOfGenerations = 50

populationSize = 10

numLinks = random.randint(7,15)

randSensorsList = [1]
for i in range(0,numLinks-1):
    randSensorsList.append(random.randint(0,1))

numSensorNeurons = randSensorsList.count(1)

numMotorNeurons = numLinks

motorJointRange = 0.5

counter = 0

past = 0

# targetPosition = -(numpy.pi)/4,
# targetPosition = random.uniform(-(numpy.pi)/2,(numpy.pi)/2),