import os
# from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER

# for i in range(0,5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

# hc = HILL_CLIMBER()
# hc.Evolve()
# hc.Show_Best()

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.plot_fitness()
phc.Show_Best()
