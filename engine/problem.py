import random as rnd

##########################################################################
# PROBLEM INTERFACE
##########################################################################
class Problem:
  def __init__(self, name_p, dimension):

    self.name      = name_p
    self.dimension = dimension

  def anySolution(self):       # Get any solution
    #solution = [0] * self.dimension
    solution = [3, 5, 8, 2, 25]
    #for j in range(self.dimension):
    #  domain      = self.domain(j)
    #  rand_index  = rnd.randint(0, len(domain)-1)
    #  solution[j] = domain[rand_index] # Assign random
    return solution

## INTERFACE ###############################
  def domain(self, index):
    pass
  def minDomain(self, index): # Min value on index domain
    pass
  def maxDomain(self, index): # Max value on index domain
    pass
  def fit_max(self, solution):  # Evaluate max objetive function
    pass
  def fit_min(self, solution):  # Evaluate min objetive function
    pass
  def fit(self, solution): # Min and Max
    pass
  def isFeasible(self, solution): # Evaluate constraints
    pass
  def isFirstBetterSecond(self, solution1, solution2):
    pass
  def evalLog(self, solution): # Solution log
    pass