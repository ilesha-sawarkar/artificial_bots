import os
#from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import pandas as pd
import gc

list_numpyseed=[6000]  #6000, 200
list_randomseed=[1000] #1000,29000
folder='experiment/Run1' #'experiment'

for i in range (len(list_numpyseed)):
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
    filename=folder+'/'+'fitness_valuesRuns'+str(10000)
    data.to_csv(filename+'.csv', index=False)
    print('Done')
    input("Press Enter To Continue")
    phc.Show_Best()
    gc.collect()
    



#for i in range(0,2):
#os.system("python3 simulate.py GUI 0 2&1 &")