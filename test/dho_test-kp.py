from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.backpack import Backpack       # Problem to solve
from algorithmSwarm.dho import DHO                      # Algorithm to use


###### MAIN ####################################
try:
  swarm = DHO(Backpack(), 100, 5)
  swarm.prepare(n_exec=300)
  swarm.solve(n_exec=100)
  swarm.bestToConsole()

except Exception as e:
  print(f"{e} \nCaused by {e.__cause__}")