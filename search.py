import os
#from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import pandas as pd


phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
print('Storing')
phc.store_best_fitness()
data=c.df
print('Saving')
print(data)
data.to_csv('fitness_valuesRuns.csv', index=False)
print('Done')
input("Press Enter To Continue")
phc.Show_Best()
pd.to_csv('data/fitness_valuesRuns.csv', c.df)


#for i in range(0,2):
#os.system("python3 simulate.py GUI 0 2&1 &")