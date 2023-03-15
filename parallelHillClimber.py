#!/usr/bin/env python3

#!/usr/bin/env python3

from solution import SOLUTION
import constants as c
import copy
import os
import pickle

class PARALLEL_HILL_CLIMBER :
	def __init__(self, runCount):
		
		self.parents = {}
		os.system("rm body/body*.urdf")
		os.system("rm brain/brain*.nndf")
		#self.parent = SOLUTION()	
		self.nextAvailableID = 0
		self.runCount= runCount
		self.fitness=[]
		self.best_fitness_runs=[]
		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID += 1
		print('Parents:\n',self.parents)
		#os.system("rm brain/brain*.nndf")
		#os.system("rm data/fitness*.nndf")
		self.currentGeneration=0
		os.system("rm fitness*.txt")
		
		
	def Evolve(self):
		self.Evaluate(solutions=self.parents, child_true=0,currentGeneration= self.currentGeneration)
		
		for currentGeneration in range(0, c.numberOfGenerations):
			self.currentGeneration=+1
			
			self.Evolve_For_One_Generation(self.currentGeneration)

			
	def Print(self):
		print("\n")
		for i in self.parents:
			print(f'parent fitness {self.parents[i].fitness} child fitness {self.children[i].fitness}')
		print("\n")
		
	def Evaluate(self,solutions, child_true, currentGeneration):
		for i in solutions:
			solutions[i].Start_Simulation("GUI", child_true)

			if(currentGeneration % 10 == 0 or currentGeneration==0):
				pass
				#solutions[i].Start_Simulation("GUI", child_true)
			else:
				solutions[i].Start_Simulation("DIRECT", child_true)
		for j in solutions:
			self.fitness.append(solutions[j].Wait_For_Simulation_To_End())
		
			
	def Evolve_For_One_Generation(self, currentGeneration):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, 1, currentGeneration)
		self.Print()
		self.Select()
		
#		self.child.Evaluate("GUI")
#		print(self.parent.fitness,self.child.fitness )
#		self.Select()
		
	def Spawn(self):
		self.children = {}
		for key in self.parents:
			self.children[key] = copy.deepcopy(self.parents[key])
			#self.children[key].Set_ID()
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
		
		with open('data/fitnessValues{0}_{1}_best.pkl'.format(str(c.numpyseed), str(c.randomseed)), 'wb') as f:
			pickle.dump(self.parents[bestParent_Key], f)
			f.close()
		
	
	def store_best_fitness(self):
		
		
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
		col_name=str(self.runCount)
		
		c.df[col_name] = best_fitness
		#c.col=c.col+1
		
		with open('data/fitnessValues{0}_{1}.pkl'.format(str(c.numpyseed), str(c.randomseed)), 'wb') as f:
			pickle.dump(best_fitness, f)
			f.close()
#			
#		ypoints = best_fitness
#		font1 = {'family':'serif','color':'blue','size':20}
#		font2 = {'family':'serif','color':'darkred','size':15}
#		plt.title("Fitness =  Negative Euclidean distance to the box/numpyseed = "+str(c.numpyseed)+"/randomseed = "+str(c.randomseed), fontdict = font1)
#		plt.xlabel("Generations", fontdict = font2)
#		plt.ylabel("Fitness", fontdict = font2)
#		plt.plot(xpoints, ypoints, marker = 'o')
#		plt.show()
		