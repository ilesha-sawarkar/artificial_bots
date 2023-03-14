#!/usr/bin/env python3

#!/usr/bin/env python3

from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER :
	def __init__(self):
		
		self.parents = {}
		
		#self.parent = SOLUTION()	
		self.nextAvailableID = 0
		self.fitness=[]
		self.best_fitness_runs=[]
		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID += 1
		print('Parents:\n',self.parents)
		os.system("rm brain/brain*.nndf")
		#os.system("rm data/fitness*.nndf")
		os.system("rm data/fitness*.txt")
		os.system("rm body/body*.urdf")
		
	def Evolve(self):
		self.Evaluate(solutions=self.parents, child_true=0)
		
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

			
	def Print(self):
		print("\n")
		for i in self.parents:
			print(f'parent fitness {self.parents[i].fitness} child fitness {self.children[i].fitness}')
		print("\n")
		
	def Evaluate(self,solutions, child_true):
		for i in range(c.populationSize):
			solutions[i].Start_Simulation("DIRECT", child_true)
			
		for i in range(c.populationSize):
			self.fitness.append(solutions[i].Wait_For_Simulation_To_End())
			
	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, 1)
		self.Print()
		self.Select()
		
#		self.child.Evaluate("GUI")
#		print(self.parent.fitness,self.child.fitness )
#		self.Select()
		
	def Spawn(self):
		self.children = {}
		for key in self.parents:
			self.children[key] = copy.deepcopy(self.parents[key])
			self.children[key].myID = self.nextAvailableID
			self.nextAvailableID += 1
			#	self.children[key] = copy.deepcopy(self.parents[parent])
			#	self.children[key].myID = self.nextAvailableID
			#	self.nextAvailableID += 1
				#self.children={}
			#for key, parent in self.parents.items():
		#	print(key, parent)
		#	self.children[key]=copy.deepcopy(parent)
			
		#	self.child = copy.deepcopy(self.parent)
		#	self.myID = self.nextAvailableID
		#	self.nextAvailableID += 1
			
	def Mutate(self):
		for key in self.children:
			self.children[key].Mutate()
			#self.child.Mutate()
		#print('\n Mutate')
		#print(self.parent.weights)
		#print(self.child.weights)
		#exit()
		
	def Select(self):
		#best=100
		for i in self.parents:
			if self.parents[i].fitness > self.children[i].fitness:
				self.parents[i] =self.children[i]
				#best= min(self.parents[i].fitness, best)
				#self.best_fitness_runs.append(best)
				
	def Show_Best(self):
		#best=float('inf')
		#min_fitness = 0
		bestParent_Key=0
		best_parent = float('inf') #self.parents[0]
		for key in self.parents:
			if best_parent > self.parents[key].fitness:
				best_parent = self.parents[key].fitness
				bestParent_Key=key
				
		print("Best Parent:",self.parents[bestParent_Key].fitness)
		
		self.parents[bestParent_Key].Start_Simulation('GUI',1)
		
	
	def store_best_fitness(self):
		x_cordinates= [i for i in range(c.numberOfGenerations+1)]
		
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
			best_fitness[i] = best_fitness[i] * -1 #-1
		col_name=str(c.col)
		c.df[col_name] = best_fitness
		c.col=c.col+1
#			
#		ypoints = best_fitness
#		font1 = {'family':'serif','color':'blue','size':20}
#		font2 = {'family':'serif','color':'darkred','size':15}
#		plt.title("Fitness =  Negative Euclidean distance to the box/numpyseed = "+str(c.numpyseed)+"/randomseed = "+str(c.randomseed), fontdict = font1)
#		plt.xlabel("Generations", fontdict = font2)
#		plt.ylabel("Fitness", fontdict = font2)
#		plt.plot(xpoints, ypoints, marker = 'o')
#		plt.show()
		