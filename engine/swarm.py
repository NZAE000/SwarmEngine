from engine.agent import Agent
from pathlib import Path
import sys
import os
import timeit

sys.path.append(str(Path(__file__).parent.parent))
#from util.minmaxMov import getMinMax
#from util.median_minmaxMov import *

##############################################################################################################
# SWARM ALGORITHM ENGINE
##############################################################################################################
class Swarm():
	def __init__(self, algorithm_name, problem, iterations, nAgents):
		
		# Algorithm + problem.
		self.id = algorithm_name + "-" + problem.name

		# Params base.
		self.maxIter     = iterations
		self.currentIter = 1
		self.nAgents     = nAgents

		# Problem.
		self.problem = problem

		# Agents.
		self.swarm = []                               # Agent storage.
		self.gBest = Agent(self.problem.dimension)    # Global Best.

		self.times_wrong = 0                          # No feasible counter.
		self.measure_time = False					  # Whether execution time should be measured

		# Members to method
		self.logIteration  = self.logIter
		self.logAgent      = self.logAgnt
		self.logGlobalBest = self.logGBest

		#self.normalize   = self.sigmoidNormalize      # Default normalization.

		# Constants needed for the problem !!
		#self.minmax_movs      = []
		#self.minmax_movs_disp = []
		#self.normalized_consts = []

		# Loggers and writers ######################################################
		# Create directories
		if not os.path.exists(str(Path(__file__).parent.parent) + "/swarm_logs/" + self.id):
			os.makedirs(str(Path(__file__).parent.parent) + "/swarm_logs/" + self.id)
		if not os.path.exists(str(Path(__file__).parent.parent) + "/data/" + self.id):
			os.makedirs(str(Path(__file__).parent.parent) + "/data/" + self.id)

		# File paths
		self.path_gbestLog     = str(Path(__file__).parent.parent) + "/swarm_logs/" + self.id + "/gbest_log"    + self.id + ".txt"
		self.path_agentLog     = str(Path(__file__).parent.parent) + "/swarm_logs/" + self.id + "/agent_log"    + self.id + ".txt"
		#self.path_movLog       = str(Path(__file__).parent.parent) + "/swarm_logs/" + self.id + "/mov_log"      + self.id + ".txt"
		self.path_gbestData    = str(Path(__file__).parent.parent) + "/data/"       + self.id + "/all_gbest"    + self.id + ".txt"
		self.path_execTimeData = str(Path(__file__).parent.parent) + "/data/"       + self.id + "/all_execTime" + self.id + ".txt"
		#self.path_minmaxData   = str(Path(__file__).parent.parent) + "/data/minmax_mov"      + self.id + ".txt"
		#self.path_constantData = str(Path(__file__).parent.parent) + "/data/constant_sigm"   + self.id + ".txt"

		# File loggers #########################################################
		self.gbestLogger = None
		self.agentLogger = None
		#self.movLogger   = None

		# File data-writers
		self.gBestWriter    = None
		self.execTimeWriter = None
		#self.minmaxWriter   = None
		#self.constantWriter = None
		########################################################################


	# HELPER METHODS ###########################################################
	def isFeasible(self, agent):
		return self.problem.isFeasible(agent.position)

	def isBetterThanGBest(self, agent):
		return self.problem.isFirstBetterSecond(agent.pBest, self.gBest.pBest)

	def isBetterThanPBest(self, agent):
		return self.problem.isFirstBetterSecond(agent.position, agent.pBest)

	# Normalize according to the specific problem
	def normalize(self, x, index):
		return self.problem.normalize(x, index)

	## SIGMOID Normalize: normalize variable on some index dimension
	#def sigmoidNormalize(self, x, index):
	#discrete_domain = self.problem.domain(index)
	#size_domain     = len(discrete_domain)
	#
	## Binary domain
	#if size_domain == 2:
	#  sigmoid = 1 / (1 + math.exp(-x)) # Sigmoid [0, 1]
	#  return self.problem.maxDomain(index) if sigmoid > rnd.random() else self.problem.minDomain(index)
	#
	## More than 2 domain values
	#print("dim: ", index)
	#print("no trans: ", x)
	#x_trans         = self.transform(x, index)
	#print("trans: ", x_trans)
	#constant        = self.normalized_consts[index]
	#sigmoid         = 1 / (1 + math.exp(-constant*x_trans)) # Sigmoid [0, 1]
	##print("mmm")
	#uniform_val = 1 / size_domain
	#acc         = uniform_val
	#chosen      = 0
	#
	#for discrete in discrete_domain:
	#  if (sigmoid <= acc):
	#    chosen = discrete
	#    break
	#  acc += uniform_val
	#
	#print("sigm: ", sigmoid, " sum: ", acc, " chosen: ", chosen, "\n")

	#return chosen

	#'''
	#Exmaple:
	#
	#  Max constants
	#  [[-7.716093991276493, 43.830473152099586], [-6.8136064932863265, 24.981377379408624], [2.142820680400068, 80.39902923747871], [-4.259218816816396, 10.548389679066661], [-10.83632385088842, 91.94979736374367]]
	#  [[-25.77328357168804, 25.77328357168804], [-15.897491936347475, 15.897491936347475], [-41.27092495893939, 41.27092495893939], [-7.403804247941528, 7.403804247941528], [-51.393060607316045, 51.393060607316045]]
	#  [0.13579953793100508, 0.2201605142505354, 0.08480546543316304, 0.4727299483874255, 0.06810257958253918]
	#
	#  Min constants
	#  [[-33.85101700085991, 13.130528711137718], [-22.354890136355586, 7.175224412439569], [-52.190351496859435, 39.33323668307838], [-7.226341827207545, 7.399602791565892], [-52.143332483418305, 64.65073983530941]]
	#  [[-23.490772855998813, 23.490772855998813], [-14.765057274397577, 14.765057274397577], [-45.76179408996891, 45.76179408996891], [-7.312972309386718, 7.312972309386718], [-58.39703615936386, 58.39703615936386]]
	#  [0.1489946721402233, 0.23704615125800804, 0.0764830153537885, 0.4786015660838073, 0.059934548569358884]
	#  
	#'''
	#
	#def transform(self, x, index):
	#  # If movement generated by pso(f.exp) was 60.0456 => Transform(rule of 3):
	#  #
	#  #                  -52.450689271945095  -   132.0017963588519     <- original range, where x is located
	#  #                  -92.22624281539849   -   92.22624281539849     <- displaced range, so transform x for this range
	#  #                  
	#  #                                     -52 |-----------------------------------------------| 132
	#  #                  -92 |-----------------------------------------------| 92
	#  #
	#  minmax      = self.minmax_movs[index]             # [-52.450689271945095, 132.0017963588519], f. exm
	#  minmax_disp = self.minmax_movs_disp[index]        # [-92.22624281539849, 92.22624281539849], f. exm
	#  #total_values   = minmax[1] - minmax[0]           # 132.0017963588519 - (-52.450689271945095) = 184.45.. => 100%
	#  value_up_to_x = x - minmax[0]                     # 60.0456 - (-52.450689271945095)           = 112.49..  => x%
	#  x_trans       = minmax_disp[0] + value_up_to_x    # => -92.22624281539849 + 112.49.. = 20.2638.. = x transformed.
	#
	#  return x_trans
	############################################################################

	# PREPARE CONSTANTS TO HELP SOLVE PROBLEM
	#def prepare(self, n_exec=30):
	#  self.normalize = self.randNormalize # Set random normalize to find min and max movements for each variable (dimensions).
	#  self.initWriters()
	# 
	#  for _ in range(n_exec): # Write min and max movement for each varable(position) of problem.
	#    self.solve()
	#    ##print("ACA?")
	#    self.writeMinMaxData(getMinMax(self.path_movLog, self.problem.dimension))
	#  
	#  self.minmaxWriter.close()
	#  # Calculate min and max movement(median) for each varable(position) of problem of all excecutions.
	#  self.minmax_movs       = getAVGMinMax(self.path_minmaxData)
	#  self.minmax_movs_disp  = displacement(self.minmax_movs)      # Apply displacement
	#  self.normalized_consts = getConstants(self.minmax_movs_disp) # Set constants to use in the normalize
	#  self.writeConstantData()
	#  
	#  self.normalize = self.sigmoidNormalize # Restore
	#  self.closeWriters()

	# RUNNER
	def solve(self, n_exec=1, measure_time=False):
		self.measure_time   = measure_time
		self.gBestWriter    = open(self.path_gbestData, "w")

		# Should time be measured? Open Writer and activate the timer.
		if self.measure_time:
			self.execTimeWriter = open(self.path_execTimeData,  "w")
			timer               = timeit.Timer(lambda: self.evolve())
			duration 			= 0
		
		# Execute n times.
		for _ in range(n_exec):
			self.init()
			if self.measure_time:
				duration = timer.timeit(number=1) # Measure self.evolve().
				self.writeExecTime(duration)
			else: 
				self.evolve()

			self.writeGBest()
			if self.measure_time == False:
				self.closeLoggers()

		# Close writers
		if self.measure_time == True:
			self.execTimeWriter.close()
		self.gBestWriter.close()
		

	# INITIALIZE SWARM #########################################################
	def init(self):
		self.initLoggers()
		self.initAgents()
		self.initGlobalBest()
		self.initialize() 	   # Initiaization in the specific algorithm.
		self.initOtherGBest()  # Initialize others global best in specific algorithm.
		self.currentIter = 1
		self.times_wrong = 0

	# INITIALIZE LOGGERS
	def initLoggers(self):
		if self.measure_time:
			self.logIteration  = lambda:       None  # Do nothing
			self.logAgent      = lambda agent: None  # Do nothing
			self.logGlobalBest = lambda:       None  # Do nothing
		else: # Activate loggers.
			self.gbestLogger = open(self.path_gbestLog, "w")
			self.agentLogger = open(self.path_agentLog, "w")
		#self.movLogger  = open(self.path_movLog,   "w")

	# CLOSE LOGGERS
	def closeLoggers(self):
		self.gbestLogger.close()
		self.agentLogger.close()
		#self.movLogger.close()

	# INIITALIZE AGENTS
	def initAgents(self):
		self.swarm.clear() # Clear agent storage

		for _ in range(self.nAgents):
			agent = Agent(self.problem.dimension) # Agents instantiated with problem dimension
			while True:
				agent.assign(self.problem.anySolution())
				if self.isFeasible(agent):
					break
			self.swarm.append(agent)

	# INITIALIZE GLOBAL BEST
	def initGlobalBest(self):
		self.gBest.copy(self.swarm[0]) # Copy first feasible agent.
		for i in range(1, self.nAgents):
			if self.isBetterThanGBest(self.swarm[i]):
				self.gBest.copy(self.swarm[i]) # Update GBest.
				#print("gbest updated")
			#else:
				#print("gbest NOT updated")

	# Run optimization
	def evolve(self):
		while self.currentIter <= self.maxIter:
			self.logIteration()				# Log current iteration.
			self.updateParams()             # Update params.
			self.updateAgents()             # Update all agents.
			self.logGlobalBest()            # Log global best.
			self.currentIter += 1           # Advance.

	# Update all agents (by default. Others algorithms can be override this method).
	def updateAgents(self):
		##print("\niter: ", self.currentIter)
		for agent in self.swarm:
			##print("before => pos: ", agent.position, " best_pos: ", agent.pBest)
			self.updateOne(agent)
			##print("after  => pos: ", agent.position, " best_pos: ", agent.pBest, "\n")

	# Update one agent.
	def updateOne(self, agent):
		backupAgent = Agent(self.problem.dimension)
		#motion_log = []

		# Move until feasible.
		while True:
			backupAgent.copy(agent)
			self.moveAgent(backupAgent)#, motion_log)
			#self.logMotion(motion_log)      # Log movement.
			#motion_log.clear()

			if self.isFeasible(backupAgent):
			#print("feasible")
				break
			else:
				#print("NO feasible")
				self.times_wrong += 1

		# Update agent.
		agent.copy(backupAgent)

		# Update pBest.
		if self.isBetterThanPBest(agent):
			agent.updatePBest()
			#print("pbest updated")
		#else:
		#  print("pbest NOT updated")

		# Update GBest.
		if self.isBetterThanGBest(agent):
			self.gBest.copy(agent)

		# Update other Gbest (in specific algorithm).
		self.checkUpdateOtherGBest(agent)
		self.logAgent(agent)


	# Agent log.
	def agentLog(self, agent):
		return self.problem.evalLog(agent.pBest)
	
	# Log global best to console.
	def bestToConsole(self):
		print(f"{self.agentLog(self.gBest)}")

# Loggers
	# Log iteration to file.
	def logIter(self):
		self.agentLogger.write(f"Iter {self.currentIter}\n")

	# Log agent to file.
	def logAgnt(self, agent):
		self.agentLogger.write(f"\tpos: {agent.position} - best_pos: {self.agentLog(agent)}\n")

	# Log global best to file.
	def logGBest(self):
		self.gbestLogger.write(f"{self.agentLog(self.gBest)}\n")

	# Log motion to file.
	#def logMotion(self, motion):
	#	self.movLogger.write(f"{motion}\n")

# Writers
	# Global best writer.
	def writeGBest(self):
		avgWrongPerAgent = self.times_wrong / (self.maxIter * self.nAgents)
		self.gBestWriter.write(f"{f"{self.agentLog(self.gBest)}-{avgWrongPerAgent}\n"}")

	# Execution time writer.
	def writeExecTime(self, duration):
		self.execTimeWriter.write(f"{duration:.6f}\n")

	## Min Max data writer
	#  def writeMinMaxData(self, minmax):
	#    self.minmaxWriter.write(f"{minmax}\n")
	#
	## Constant data writer
	#  def writeConstantData(self):
	#    self.constantWriter.write(f"{self.minmax_movs}\n")
	#    self.constantWriter.write(f"{self.minmax_movs_disp}\n")
	#    self.constantWriter.write(f"{self.normalized_consts}\n")

	## Initialize writers
	#  def initWriters(self):
	#    self.closeWriters()
	#    self.minmaxWriter   = open(self.path_minmaxData, "w")
	#    self.constantWriter = open(self.path_constantData, "w")

	## Close writers
	#  def closeWriters(self):
	#    self.minmaxWriter.close()
	#    self.constantWriter.close()

## INTERFACE #################################################

	# INIT REQUERIED MEMBERS IN SPECIFI ALGORITHM.
	def initialize(self):
		pass
	
	# INIT OTHERS GBest.
	def initOtherGBest(self):
		pass

	# UPDATE PARAMETERS.
	def updateParams(self):
		pass

	# MOVE: the implementer should append the pos+perturbance for each dimension to 'motion_log'.
	def moveAgent(self, agent):#, motion_log):
		pass

	# UPDATE OTHERS GBest.
	def checkUpdateOtherGBest(self, agent):
		pass
