#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues= np.load('data/backLegSensorValues.npy')
frontLegSensorValues= np.load('data/frontLegSensorValues.npy')
plt.plot(backLegSensorValues, label='backLegSensorValues')
plt.plot(frontLegSensorValues, label='frontLegSensorValues', linewidth=2)
plt.legend()
plt.show()