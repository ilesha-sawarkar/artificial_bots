import os
#from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import pandas as pd
import gc

list_numpyseed=[600, 20,90,70,80]
list_randomseed=[1000,29000,6000,90000,100]

for i in range (0,5):
    gc.collect()
    
    c.numpyseed=list_numpyseed[i]
    c.randomseed=list_randomseed[i]
    print('NUMPY_SEED', c.numpyseed)
    print('RANDOM_Seeed', c.randomseed)
    phc = PARALLEL_HILL_CLIMBER(runCount=i)
    phc.Evolve()
    print('Storing')
    phc.store_best_fitness()
    data=c.df
    print('Saving')
    print(data)
    filename='fitness_valuesRuns'+str(i)
    data.to_csv(filename+'.csv', index=False)
    print('Done')
    input("Press Enter To Continue")
    phc.Show_Best()
    gc.collect()



#for i in range(0,2):
#os.system("python3 simulate.py GUI 0 2&1 &")