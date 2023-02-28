import os
from solution import SOLUTION
import constants as c
import copy
import matplotlib.pyplot as plt


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")
        self.nextAvailableID = 0
        self.parents = {}
        self.fitness = []
        # self.parent = SOLUTION()
        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
        
    def Evolve(self):
        self.Evaluate(self.parents, 0)
        for currentGeneration in range(0,c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        
    
    def Evolve_For_One_Generation(self):
        pass
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, 1)
        # self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for k in self.parents:
            self.children[k] = copy.deepcopy(self.parents[k])
            self.children[k].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

        # self.child = copy.deepcopy(self.parent) 
        # self.child.Set_ID(self.nextAvailableID)
        # self.nextAvailableID = self.nextAvailableID + 1

    def Mutate(self):
        for l in self.children:
            self.children[l].Mutate()
        # self.child.Mutate()

    def Select(self):
         for n in self.parents:
            if(self.parents[n].fitness > self.children[n].fitness):
                self.parents[n] = self.children[n]

    def Print(self):
        for m in self.parents:
            print("Parent's fitness : ", self.parents[m].fitness,"  | Child's fitness : ", self.children[m].fitness)

    def Show_Best(self):
        best = float('inf')
        alpha = None
        for o in self.parents:
            if best > self.parents[o].fitness:
                best = self.parents[o].fitness
                alpha = o
        print("Besttttt:",self.parents[alpha].fitness)
        self.parents[alpha].Start_Simulation("GUI",1)
        # self.parent.Evaluate("GUI")

    def Evaluate(self, solutions, child_true):
        for i in solutions:
           solutions[i].Start_Simulation("DIRECT", child_true)
        for j in solutions:
            self.fitness.append(solutions[j].Wait_For_Simulation_To_End())
        pass

    def plot_fitness(self):
        xpoints = [i for i in range(c.numberOfGenerations + 1)]
        fitness_population = []
        counter = 0
        best_fitness = []
        for i in range(len(self.fitness)):
            fitness_population.append(self.fitness[i])
            counter +=1
            if counter == c.populationSize:
                best_fitness.append(min(fitness_population))
                counter = 0
                
        for i in range(len(best_fitness)):
            best_fitness[i] = int(best_fitness[i] * -1)
            
        ypoints = best_fitness
        font1 = {'family':'serif','color':'blue','size':20}
        font2 = {'family':'serif','color':'darkred','size':15}
        plt.title("Fitness =  Negative Euclidean distance to the box/numpyseed = "+str(c.numpyseed)+"/randomseed = "+str(c.randomseed), fontdict = font1)
        plt.xlabel("Generations", fontdict = font2)
        plt.ylabel("Fitness", fontdict = font2)
        plt.plot(xpoints, ypoints, marker = 'o')
        plt.show()

        