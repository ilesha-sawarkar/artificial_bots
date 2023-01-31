import os
from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()

#for i in range(0,2):
#os.system("python3 simulate.py GUI 0 2&1 &")