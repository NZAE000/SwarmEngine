import math
import random as rnd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.problem import Problem


##########################################################################
# ADVERTISEMENTS PROBLEM
##########################################################################
class Advertisements(Problem):
  def __init__(self):
    super().__init__("ads", 5) # Name problem and dimension params

    self.costs   = [160, 300, 40, 100, 10]
    self.values  = [65, 90, 40, 60, 20]

    # Best values and weights(priority) of objetive functions
    self.bestMax = 3200         # Best value achieved to maximize
    self.bestMin = 0            # Best value achieved to minimize
    self.weights = [1, 0]     	# [0] = max; [1] = min

    self.domains = {
      0: (0, 15), # = 16 vals => 15 partitions (1/15)
      1: (0, 10),
      2: (0, 25),
      3: (0,  4),
      4: (0, 30)
    }

    self.constraints = { # map(key, value)
        "c1": lambda x1, x2: ( self.costs[0]*x1 + self.costs[1]*x2 <= 3800 ),
        "c2": lambda x3, x4: ( self.costs[2]*x3 + self.costs[3]*x4 <= 2800 ),
        "c3": lambda x3, x5: ( self.costs[2]*x3 + self.costs[4]*x5 <= 3500 )
    }


# IMPLEMENTS! #########################################################
  def domain(self, index):
    return [ val for val in range(self.minDomain(index), self.maxDomain(index)+1) ]
  
  def minDomain(self, index):       # Min value on index domain
    return self.domains[index][0]
  
  def maxDomain(self, index):       # Max value on index domain
    return self.domains[index][1]

  def fit_max(self, solution):      # Evaluate max objetive function
    sum = 0
    for i in range(self.dimension):
        sum += solution[i] * self.values[i]
    return sum

  def fit_min(self, solution):      # Evaluate min objetive function
    sum = 0
    for i in range(self.dimension):
        sum += solution[i] * self.costs[i]
    return sum

  def fit(self, solution): # Min and Max
    # Adjustment variables.
    c_hat   = 10000   # Upper bound of the minimization objective function.
    fit_max = self.fit_max(solution)
    fit_min = self.fit_min(solution)

    scalarized_fit = 0
    #size_w         = len(self.weights)
    #for p in range(size_w):
    #  for q in range(size_w):
    #    if p != q:
    term_max = (fit_max / self.bestMax) * self.weights[0]
    term_min = (c_hat - fit_min) / (c_hat - self.bestMin) * self.weights[1]
    scalarized_fit += term_max + term_min

    return fit_max
  
  def isFirstBetterSecond(self, solution1, solution2):
    return (self.fit(solution1) > self.fit(solution2))
  
  def isFeasible(self, solution): # Evaluate constraints
    c1_okey = self.constraints["c1"](solution[0], solution[1])
    c2_okey = self.constraints["c2"](solution[2], solution[3])
    c3_okey = self.constraints["c3"](solution[2], solution[4])
    #print("Faseable?:", c1_okey, c2_okey, c3_okey)
    return (c1_okey and c2_okey and c3_okey)
  
  # Solution log
  def evalLog(self, solution):
    cost  = self.fit_min(solution)
    value = self.fit_max(solution)
    return f"{self.fit(solution)}-{solution}-{cost}-{value}"
  
  # SIGMOID: normalize variable on some index dimension.
  def normalize(self, x, index):
    discrete_domain = self.domain(index)
    probs = []
    for _ in range(len(discrete_domain)):
        probs.append(1 / (1 + math.exp(-(x + rnd.gauss(0, 0.5)))))

    total = sum(probs)
    normalized = [p / total for p in probs]

    # Proportional sampling
    r = rnd.random()
    acc = 0
    for i, p in enumerate(normalized):
        acc += p
        if r <= acc:
            return discrete_domain[i]
    return discrete_domain[len(discrete_domain)-1]
