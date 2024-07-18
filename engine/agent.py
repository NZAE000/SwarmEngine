##########################################################################
# AGENT
##########################################################################
class Agent:
  def __init__(self, dimension):
    # Each agent has position, velocity and best-position in n dimension
    self.dimension = dimension
    self.position  = [0] * self.dimension  # Represents values ​​of each variable of interest
    self.velocity  = [0] * self.dimension
    self.pBest     = [0] * self.dimension

  # Assign agent with some solution
  def assign(self, solution):
    if len(solution) == self.dimension:
      for j in range(self.dimension):
        self.position[j] = solution[j]           
        self.pBest[j]    = self.position[j]
        self.velocity[j] = 0             # Velocity vector at 0 initially

  def updatePBest(self):
    for j in range(self.dimension):
      self.pBest[j] = self.position[j]

  def copy(self, other):
    for j in range(self.dimension):
      self.position[j] = other.position[j]
      self.velocity[j] = other.velocity[j]
      self.pBest[j]    = other.pBest[j]
