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
		self.best_fitness_runs=[]
		for i in range(c.populationSize):
				self.parents[i] = SOLUTION(self.nextAvailableID)
				self.nextAvailableID += 1
		print(self.parents)
		os.system("rm brain*.nndf")
		os.system("rm data/fitness*.nndf")
		
	def Evolve(self):
		self.Evaluate(self.parents, "GUI")
		
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

			
	def Print(self):
		print("\n")
		for i in self.parents:
			print(f'parent fitness {self.parents[i].fitness} child fitness {self.children[i].fitness}')
		print("\n")
		
	def Evaluate(self,solutions, mode):
		for i in range(c.populationSize):
			solutions[i].Start_Simulation(mode)
			
		for i in range(c.populationSize):
			solutions[i].Wait_For_Simulation_To_End()
			
	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, "DIRECT")
		self.Print()
		self.Select()
		
#		self.child.Evaluate("GUI")
#		print(self.parent.fitness,self.child.fitness )
#		self.Select()
		
	def Spawn(self):
		self.children = {}
		for key, parent in self.parents.items():
			self.children[key] = copy.deepcopy(parent)
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
		for key, child in self.children.items():
			child.Mutate()
			#self.child.Mutate()
		#print('\n Mutate')
		#print(self.parent.weights)
		#print(self.child.weights)
		#exit()
		
	def Select(self):
		best=100
		for i in self.parents:
			if self.parents[i].fitness > self.children[i].fitness:
				self.parents[i] =self.children[i]
			best= min(self.parents[i].fitness, best)
			self.best_fitness_runs.append(best)
				
	def Show_Best(self):
		#min_fitness = 0
		best_parent = self.parents[0]
		for key, parent in self.parents.values():
			if best_parent.fitness > parent.fitness:
				best_parent = parent
		
		best_parent.Start_Simulation('GUI')