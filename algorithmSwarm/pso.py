from pathlib import Path
import random as rnd
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.swarm import Swarm

# SUBFIGURE (GRAPH LATEX)

##########################################################################
# PSO ALGORITHM
##########################################################################
class PSO(Swarm):
  def __init__(self, problem, iterations, nAgents):
    super().__init__("PSO", problem, iterations, nAgents)

    # Params PSO (0.9, 2, 2) (default)
    self.theta = 0.9 #[0, 1]
    self.alpha = 2
    self.beta  = 2


# IMPLEMENTS! #########################################################
  # MOVE
  def moveAgent(self, agent, motion_log):
    
    for j in range(self.problem.dimension):
      agent.velocity[j] = self.theta * agent.velocity[j] + self.alpha * rnd.random() * (self.gBest.position[j] - agent.position[j]) + self.beta * rnd.random() * (agent.pBest[j] - agent.position[j])
      next_pos          = agent.position[j] + agent.velocity[j]
      agent.position[j] = self.normalize(next_pos, j) # Update position (normalized to the problem domain)

      motion_log.append(next_pos)
