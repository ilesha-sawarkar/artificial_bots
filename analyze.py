#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

randomseed=[]
numpyseed=[]

experiment= pd.read_csv('experiment/fitness_valuesRuns.csv')
control=pd.read_csv('control/fitness_valuesRuns.csv')


control.tail()
control.rename(columns={"0": "6000", "1": "8000","2": "200", "3": "90","4": "400"})
control.drop(columns=['Generation'],inplace=True)
experiment.drop(columns=['Generation'],inplace=True)
control_cols=control.columns
experiment_col=experiment.columns
for column in control_cols:
	for i in range(0, len(control[column])):
		control[column][i]=math.floor(control[column][i])
		
for column in experiment_col:
	for i in range(0, len(experiment[column])):
		experiment[column][i]=math.floor(experiment[column][i])

control.rename(columns={"0": "6000", "1": "8000","2": "200", "3": "90","4": "400"},inplace=True)
experiment.rename(columns={"0": "6000", "1": "8000","2": "200", "3": "90","4": "400"}, inplace=True)
control.plot(kind='line', title="Control")
experiment.plot (kind='line',title="Experiment")
#plt.plot(backLegSensorValues, label='backLegSensorValues')
#plt.plot(frontLegSensorValues, label='frontLegSensorValues', linewidth=2)
plt.legend()
plt.show()