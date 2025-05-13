import math
import random as rnd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.problem import Problem


'''
pso

[0.5, 0.5]
[[-29.966662413041238, 179.4587208934107], [-76.75902024909554, 44.39881860953902], [4.702968903148879, 338.3706019384982], [-16.491573881549453, 37.876169212744564], [9.502259592281737, 394.0147364456316]]
[[-104.71269165322597, 104.71269165322597], [-60.57891942931728, 60.57891942931728], [-171.53678542082355, 171.53678542082355], [-27.183871547147007, 27.183871547147007], [-201.7584980189567, 201.7584980189567]]
[0.03342479258952535, 0.0577758737358093, 0.020403786811170596, 0.12875281557778442, 0.017347472519701]

[1, 0]
[[-18.89653477805245, 177.4978608939855], [-21.12575932936682, 92.49872868643925], [0.6853774780984564, 323.8605403592637], [-15.358727169897255, 38.485726201975105], [-21.849275174364195, 364.48669926393296]]
[[-98.19719783601897, 98.19719783601897], [-56.81224400790303, 56.81224400790303], [-162.2729589186811, 162.2729589186811], [-26.92222668593618, 26.92222668593618], [-193.16798721914859, 193.16798721914859]]
[0.03564256493189046, 0.06160643820921987, 0.021568596661591256, 0.13000410556041986, 0.018118944294994693]

[0, 1]
[[-167.04722153210088, 9.55033677176933], [-110.43688268354967, 7.2868076461283335], [-269.8438324877572, 62.60920386439518], [-32.27320818301845, 21.905708796459184], [-246.12673826239032, 182.07960411811516]]
[[-88.29877915193511, 88.29877915193511], [-58.861845164839, 58.861845164839], [-166.22651817607618, 166.22651817607618], [-27.089458489738817, 27.089458489738817], [-214.10317119025274, 214.10317119025274]]
[0.039638147136525796, 0.05946126884399332, 0.02105560555802901, 0.12920154905738557, 0.01634725903657863]

'''

##########################################################################
# ADVERTISEMENTS PROBLEM
##########################################################################
class Advertisements(Problem):  # T2-advertisements
  def __init__(self):
    super().__init__("ads", 5) # Name problem and dimension params

    self.costs   = [160, 300, 40, 100, 10]
    self.values  = [65, 90, 40, 60, 20]

    # Best values and weights(priority) of objetive functions
    self.bestMax = 3200           # Mejor valor alcanzado para maximizar
    self.bestMin = 0              # Mejor valor alcanzado para minimizar
    self.weights = [0.5, 0.5]         # [0] = max; [1] = min

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
    return [ val for val in range(self.minDomain(index), self.maxDomain(index)) ]
  
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
    # Variables de ajuste
    c_hat   = 10000   # Cota superior de la función objetivo de minimización
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
  
  def isFeasible(self, solution): # Evaluate constraints
    c1_okey = self.constraints["c1"](solution[0], solution[1])
    c2_okey = self.constraints["c2"](solution[2], solution[3])
    c3_okey = self.constraints["c3"](solution[2], solution[4])
    #print(c1_okey, c2_okey, c3_okey)
    return (c1_okey and c2_okey and c3_okey)
  
  def isFirstBetterSecond(self, solution1, solution2):
    return (self.fit(solution1) > self.fit(solution2))
  
  def evalLog(self, solution): # Solution log
    cost  = self.fit_min(solution)
    value = self.fit_max(solution)
    return f"{self.fit(solution)}-{solution}-{cost}-{value}"
