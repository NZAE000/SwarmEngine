import math
import random as rnd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.problem import Problem


'''
[0.5, 0.5]
[[-26.33878694942603, 182.0818601093577], [-78.06010697221623, 42.02544522941313], [9.781921813108777, 338.03298098745677], [-17.372683783150933, 36.60430489249712], [5.53553133978934, 392.5155464976713]]
[[-104.21032352939187, 104.21032352939187], [-60.04277610081468, 60.04277610081468], [-173.90745140028278, 173.90745140028278], [-26.988494337824026, 26.988494337824026], [-199.02553891873032, 199.02553891873032]]
[0.028787934807187013, 0.04996437864503229, 0.017250554682069947, 0.11115847970057147, 0.015073442414970743]

[1, 0]
[[-14.970173484676415, 179.47329661776456], [-19.64284466768485, 90.6182532522313], [6.5562770117811375, 325.10537769960456], [-15.931187753535456, 38.051362459487265], [-23.829500057043703, 361.8532371755746]]
[[-97.22173505122049, 97.22173505122049], [-55.13054895995808, 55.13054895995808], [-165.83082735569286, 165.83082735569286], [-26.99127510651136, 26.99127510651136], [-192.84136861630913, 192.84136861630913]]
[0.03085729748002825, 0.05441629108715992, 0.01809072563791326, 0.11114702762880149, 0.015556827985228693]

[0, 1]

[[-170.17973548803712, 11.069606581089525], [-110.85938244714762, 5.179499402801352], [-266.66195333891335, 63.597237175280995], [-32.80417863517925, 22.066069838295853], [-246.3468988407406, 176.6793581227258]]
[[-90.62467103456332, 90.62467103456332], [-58.01944092497449, 58.01944092497449], [-165.12959525709718, 165.12959525709718], [-27.43512423673755, 27.43512423673755], [-211.5131284817332, 211.5131284817332]]
[0.03310356844060522, 0.051706806411308405, 0.018167548920162823, 0.10934887606533197, 0.014183516746853317]

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
    size_w         = len(self.weights)
    for p in range(size_w):
      for q in range(size_w):
        if p != q:
          term_max = (fit_max / self.bestMax) * self.weights[0]
          term_min = (c_hat - fit_min) / (c_hat - self.bestMin) * self.weights[1]
          scalarized_fit += term_max + term_min

    return scalarized_fit
  
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
