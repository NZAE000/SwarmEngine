import math
import random as rnd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.problem import Problem


##########################################################################
# PICK-UP PROBLEM:
#    In last-mile logistics, an effective strategy is to establish temporary 
#    microhubs as pickup points where customers can retrieve their orders. 
#    This reduces direct distribution costs, consolidates deliveries, and 
#    improves coverage in areas with access challenges or high dispersion.
##########################################################################
class Pickup(Problem):
	def __init__(self):

		'''# Small #################################################################
		super().__init__("pickup", 6) # Name problem and dimension params.

		self.n_clients = self.dimension
		self.n_hubs    = 3
		# Best values and weights(priority) of objetive functions
		self.bestMax = 63           # Best value achieved to maximize
		self.bestMin = 0            # Best value achieved to minimize
		self.weights = [0.35, 0.65]       # [0] = max; [1] = min

		# Client-hub distance matrix
		self.distances = [
			[5, 8, 11],
			[7, 4, 10],
			[6, 6, 6],
			[9, 5, 7],
			[8, 9, 5],
			[4, 7, 12]
		]

		self.costs        = [20, 25, 15]   # Fixed cost for opening each hub.
		self.value        = [5, 10, 5]    # Fixed value for opening each hub.
		self.capabilities = [2, 3, 2]      # Maximum service capacity per hub.
		self.D_max        = 8              # Maximum tolerated distance between client and hub.'''

		# Medium #################################################################
		super().__init__("pickup", 12) # Name problem and dimension params.

		self.n_clients = self.dimension
		self.n_hubs    = 5
		# Best values and weights(priority) of objetive functions
		self.bestMax = 136           # Best value achieved to maximize
		self.bestMin = 0            # Best value achieved to minimize
		self.weights = [0.6, 0.4]       # [0] = max; [1] = min

		# Client-hub distance matrix
		self.distances = [
			[6, 9, 12, 7, 8],
			[5, 8, 6, 10, 9],
			[8, 7, 9, 6, 11],
			[7, 5, 6, 9, 10],
			[9, 6, 8, 12, 7],
			[6, 5, 9, 11, 8],
			[8, 7, 5, 6, 10],
			[7, 6, 9, 8, 6],
			[5, 9, 10, 7, 11],
			[9, 6, 7, 8, 9],
			[6, 10, 8, 7, 5],
			[8, 6, 9, 10, 6]
		]

		self.costs        = [20, 25, 18, 22, 19]   	# Fixed cost for opening each hub.
		self.value        = [5, 10, 5, 8, 6]    	# Fixed value for opening each hub.
		self.capabilities = [3, 3, 3, 3, 3]      	# Maximum service capacity per hub.
		self.D_max        = 9             			# Maximum tolerated distance between client and hub.'''

		# Hard #################################################################
		'''super().__init__("pickup", 24) # Name problem and dimension params.

		self.n_clients = self.dimension
		self.n_hubs    = 8
		# Best values and weights(priority) of objetive functions
		self.bestMax = 200           	# Best value achieved to maximize
		self.bestMin = 0            	# Best value achieved to minimize
		self.weights = [0.6, 0.4]       # [0] = max; [1] = min

		# Client-hub distance matrix
		self.distances = [
			[6, 8, 12, 7, 9, 6, 10, 11],
			[5, 9, 6, 10, 8, 7, 9, 12],
			[8, 7, 10, 6, 11, 9, 8, 10],
			[7, 6, 8, 9, 10, 6, 7, 9],
			[9, 6, 9, 12, 7, 10, 11, 8],
			[6, 5, 10, 11, 9, 8, 6, 7],
			[8, 7, 6, 6, 10, 8, 9, 9],
			[7, 6, 10, 8, 6, 9, 11, 10],
			[5, 9, 11, 7, 11, 8, 10, 12],
			[9, 6, 7, 8, 9, 6, 10, 8],
			[6, 10, 8, 7, 5, 9, 6, 8],
			[8, 6, 9, 10, 6, 8, 10, 7],
			[7, 9, 10, 8, 11, 9, 7, 8],
			[6, 7, 8, 9, 10, 8, 9, 11],
			[9, 8, 6, 10, 7, 6, 9, 10],
			[7, 6, 9, 8, 10, 7, 6, 9],
			[8, 9, 10, 6, 11, 10, 8, 7],
			[9, 7, 6, 9, 10, 8, 7, 6],
			[6, 8, 7, 10, 9, 7, 8, 6],
			[8, 9, 10, 8, 9, 10, 9, 7],
			[7, 6, 8, 9, 7, 9, 10, 8],
			[5, 9, 11, 10, 9, 7, 8, 6],
			[6, 8, 7, 9, 6, 10, 11, 9],
			[8, 7, 9, 8, 10, 8, 7, 6],
		]

		self.costs        = [22, 25, 18, 20, 19, 24, 21, 23]   	# Fixed cost for opening each hub.
		self.value        = [5, 10, 5, 8, 6, 6, 11, 4, 12]      # Fixed value for opening each hub.
		self.capabilities = [4, 4, 4, 4, 4, 3, 4, 3]      		# Maximum service capacity per hub.
		self.D_max        = 9             						# Maximum tolerated distance between client and hub.'''


	# IMPLEMENTS! #########################################################
	def domain(self, index):
		return [ val for val in range(self.minDomain(index), self.maxDomain(index)+1) ]

	def minDomain(self, index):       # Min value on index domain.
		return 0

	def maxDomain(self, index):       # Max value on index domain.
		return self.n_hubs-1

	def fit_max(self, solution):      # Evaluate max objetive function.
		# Derive hubs from assignments.
		hubs = []
		for _ in range(self.n_hubs):
			hubs.append(0)

		for h in solution: # Activate hubs used by clients (solution = [hub_to_c1, hub_to_c2, ..., hub_to_cn]).
			hubs[h] = 1

		# Calculate total assignment distance.
		total = 0
		for c in range(self.n_clients):
			total += self.distances[c][solution[c]]

		# Add fix service value.
		for j in range(self.n_hubs):
			if hubs[j] == 1:
				total += self.value[j]
		
		return total

	def fit_min(self, solution):      # Evaluate min objetive function.
		# Derive hubs from assignments.
		hubs = []
		for _ in range(self.n_hubs):
			hubs.append(0)

		for h in solution: # Activate hubs used by clients (solution = [hub_to_c1, hub_to_c2, ..., hub_to_cn]).
			hubs[h] = 1

		# Calculate total assignment distance.
		total = 0
		for c in range(self.n_clients):
			total += self.distances[c][solution[c]]

		# Add fixed cost of activated hubs.
		for j in range(self.n_hubs):
			if hubs[j] == 1:
				total += self.costs[j]

		return total

	def fit(self, solution): # Min and Max.
		# Adjustment variables.
		c_hat   = 100   # Upper bound of the minimization objective function.
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

		return fit_min

	def isFirstBetterSecond(self, solution1, solution2):
		return (self.fit(solution1) < self.fit(solution2))

	def isFeasible(self, solution): # Evaluate constraints.
		# Derive hubs from assignments.
		hubs = []
		for _ in range(self.n_hubs):
			hubs.append(0)
		for h in solution:
			hubs[h] = 1

		# Check capacity and maximum distance.
		count = [0] * self.n_hubs
		for c in range(self.n_clients):
			h = solution[c]

			# Check maximum distance.
			if self.distances[c][h] > self.D_max:
				return False

			# Hub must be active (already fulfilled by construction).
			count[h] += 1
			if count[h] > self.capabilities[h]:
				return False

		return True

	# Solution log.
	def evalLog(self, solution):
		cost  = self.fit_min(solution)
		value = self.fit_max(solution)
		return f"{self.fit(solution)}-{solution}-{cost}-{value}"

	# SIGMOID: normalize variable on some index dimension.
	def normalize(self, x, index):
		probs = []
		for _ in range(self.n_hubs):
			probs.append(1 / (1 + math.exp(-(x + rnd.gauss(0, 0.5)))))

		total      = sum(probs)
		normalized = [p / total for p in probs]

		# Proportional sampling
		r = rnd.random()
		acc = 0
		for i, p in enumerate(normalized):
			acc += p
			if r <= acc:
				return i
		return self.n_hubs-1
