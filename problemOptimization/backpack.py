import math
import random as rnd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.problem import Problem

##########################################################################
# BACKPACK PROBLEM
##########################################################################
class Backpack(Problem):  # T2-advertisements
	def __init__(self):
		super().__init__("kp", 10) # Name problem and dimension params

		self.values   = [55,10,4,75,4,50,8,61,85,87]
		self.weight   = [95,4,60,32,23,72,80,62,65,46]
		self.capacity = 269

		self.dom = (0, 1)

	# IMPLEMENTS! #########################################################
	def domain(self, index):
		return [ self.dom[0], self.dom[1] ]

	def minDomain(self, index):     # Min value on index domain
		return self.dom[0]

	def maxDomain(self, index):     # Max value on index domain
		return self.dom[1]

	def fit_max(self, solution):    # Evaluate max objetive function
		sum = 0
		for j in range(self.dimension):
			sum += solution[j] * self.values[j]
		return sum

	def fit_min(self, solution): # Evaluate min objetive function
		pass

	def fit(self, solution):
		return self.fit_max(solution)

	def evalConstraint(self, solution):
		sum = 0
		for j in range(self.dimension):
			sum += solution[j] * self.weight[j]
		return sum

	def isFeasible(self, solution): # Evaluate constraints
		return self.evalConstraint(solution) <= self.capacity

	def isFirstBetterSecond(self, solution1, solution2):
		return (self.fit(solution1) >= self.fit(solution2))

	# SIGMOID normalize: choose 0 and 1.
	def normalize(self, x, index):
		sigmoid = 1 / (1 + math.exp(-x)) # Sigmoid [0, 1]
		return self.maxDomain(index) if sigmoid > rnd.random() else self.minDomain(index)

	def evalLog(self, solution): # Eval solution log
		return f"fitness: {self.fit(solution)} - {solution} - total_weight: {self.evalConstraint(solution)}"