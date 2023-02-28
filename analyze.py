import numpy
import matplotlib.pyplot


backLegSensorValues = numpy.load("./data/backLegSensorValues.npy")
# print(backLegSensorValues)


frontLegSensorValues =  numpy.load("./data/frontLegSensorValues.npy") 

targetAnglesBackLeg =  numpy.load("./data/targetAnglesBackLeg.npy") 
targetAnglesFrontLeg =  numpy.load("./data/targetAnglesFrontLeg.npy") 


# matplotlib.pyplot.plot(backLegSensorValues, label='Back Leg', linewidth=3)
# matplotlib.pyplot.plot(frontLegSensorValues, label='Front Leg')
# matplotlib.pyplot.legend()

matplotlib.pyplot.plot(targetAnglesBackLeg, label='Back Leg')
matplotlib.pyplot.plot(targetAnglesFrontLeg, label='Front Leg')
matplotlib.pyplot.legend()

matplotlib.pyplot.show()