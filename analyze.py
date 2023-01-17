#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

#backLegSensorValues= np.load('data/backLegSensorValues.npy')
#frontLegSensorValues= np.load('data/frontLegSensorValues.npy')
targetAngles_BackLeg=np.load('data/targetAngles_BackLeg.npy')
targetAngles_FrontLeg=np.load('data/targetAngles_FrontLeg.npy')

plt.plot(targetAngles_BackLeg, label='targetAngles_BackLeg')
plt.plot(targetAngles_FrontLeg, label='targetAngles_FrontLeg')

#plt.plot(backLegSensorValues, label='backLegSensorValues')
#plt.plot(frontLegSensorValues, label='frontLegSensorValues', linewidth=2)
plt.legend()
plt.show()