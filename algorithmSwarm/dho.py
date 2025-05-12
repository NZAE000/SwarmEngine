import math
from pathlib import Path
import random as rnd
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.swarm import Swarm
from engine.agent import Agent


##########################################################################
# DHO ALGORITHM
##########################################################################
class DHO(Swarm):
  def __init__(self, problem, iterations, nAgents):
    super().__init__("DHO", problem, iterations, nAgents)

# Variable params for each iteration
    self.beta          = 0 # rand(-1, 1)
    self.tau           = 0 # rand(0, 1)
    self.lambd         = 0 # rand(0, 1)

    self.windAngle     = 0 # 2 * phi * lambd
    self.windSpeed     = 0 # Sw = rand(0, 2)
    self.deerAnglePos  = 0 # phi + windAngle
    self.deerAngleView = 0 # 1/8 * phi * lambd
    self.deltaAngle    = 0 # windAngle - deerAngleView

    # Coef. vectors
    self.Y = 0  # 0.25 * log(Iter + 1 / maxIter) * beta
    self.L = 0  # 2 * tau

# Agents
    # geleader(gBest) in the super class
    self.gSuccesor = Agent(self.problem.dimension)      # Second g best
    self.move      = self.moveBasedLeader               # Default

  # HELPER METHOD ###########################################################
  def isBetterThanGSuccesor(self, agent):
    return self.problem.isFirstBetterSecond(agent.pBest, self.gSuccesor.position)
  ############################################################################
  
  def findGLeader(self):
    super().findGBest()

  def findGSuccesor(self):
    for i in range(self.nAgents):
      if self.isBetterThanGSuccesor(self.swarm[i]) and not self.isBetterThanGBest(self.swarm[i]):
        self.gSuccesor.copy(self.swarm[i])

  def chooseMovement(self):
    if self.windSpeed < 1:
      if abs(self.L) >= 1:
        return self.moveBasedLeader
      else:
        return self.moveBasedSuccesor
    else:
      return self.moveBasedAngle

  def moveBasedLeader(self, agent, motion_log):
    for j in range(self.problem.dimension):
      # Change params
      self.beta = rnd.randint(-1, 1)
      self.Y    = 0.25 * math.log(self.currentIter + (1 / self.maxIter)) * self.beta

      next_pos    = self.gBest.position[j] - self.Y * self.windSpeed * abs(self.L * self.gBest.position[j] * agent.position[j])
      agent.position[j] = self.normalize(next_pos, j)
      
      motion_log.append(next_pos)

  def moveBasedSuccesor(self, agent, motion_log):
    for j in range(self.problem.dimension):
      # Change params
      self.beta = rnd.randint(-1, 1)
      self.Y    = 0.25 * math.log(self.currentIter + (1 / self.maxIter)) * self.beta

      next_pos    = self.gSuccesor.position[j] - self.Y * self.windSpeed * abs(self.L * self.gBest.position[j] * agent.position[j])
      agent.position[j] = self.normalize(next_pos, j)
      
      motion_log.append(next_pos)

  def moveBasedAngle(self, agent, motion_log):
    for j in range(self.problem.dimension):
      # Change params
      self.lambd         = rnd.randint(0, 1)
      self.windAngle     = 2 * math.pi * self.lambd
      self.deerAnglePos  = math.pi + self.windAngle

      self.deerAngleView = 1/8 * math.pi * self.lambd
      self.deltaAngle    = self.windAngle - self.deerAngleView
      self.deerAnglePos  = self.deerAnglePos + self.deltaAngle

      self.beta = rnd.randint(-1, 1)
      self.Y    = 0.25 * math.log(self.currentIter + (1 / self.maxIter)) * self.beta

      next_pos    = self.gBest.position[j] + self.Y * self.windSpeed * abs(math.cos(self.deerAnglePos) * self.gBest.position[j] - agent.position[j])
      agent.position[j] = self.normalize(next_pos, j)
      
      motion_log.append(next_pos)

# IMPLEMENTS! #########################################################

# MOVE
  def moveAgent(self, agent, motion_log):
    self.move(agent, motion_log)

# UPDATE PARAMETERS
  def updateParams(self):
    #self.beta         = rnd.randint(-1, 1)
    self.tau       = rnd.randint(0, 1)
    #self.lambd        = rnd.randint(0, 1)
    #self.windAngle    = 2 * math.pi * self.lambd

    self.windSpeed = rnd.randint(0, 2)

    #self.deerAnglePos = math.pi + self.windAngle

    ## Coef. vectors
    #self.Y = 0.25 * math.log(self.currentIter + (1 / self.maxIter)) * self.beta
    self.L = 2 * self.tau
    self.move = self.chooseMovement()

# SEARCH G
  def findGBest(self):
    self.findGLeader()
    self.findGSuccesor()
  
# Reset global
  def initGBest(self):
    super().initGBest()
    self.gSuccesor.copy(self.swarm[0])  # Copy first feasible agent