#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

randomseed=[]
numpyseed=[]

experiment= pd.read_csv('/Users/ilesha/AndroidStudioProjects/GITHUB\ SYNC/artificial_bots/experiment/fitness_valuesRuns.csv')
control=pd.read_csv('/Users/ilesha/AndroidStudioProjects/GITHUB\ SYNC/artificial_bots/control/fitness_valuesRuns.csv')
plt.plot(targetAngles_BackLeg, label='targetAngles_BackLeg')
plt.plot(targetAngles_FrontLeg, label='targetAngles_FrontLeg')

#plt.plot(backLegSensorValues, label='backLegSensorValues')
#plt.plot(frontLegSensorValues, label='frontLegSensorValues', linewidth=2)
plt.legend()
plt.show()