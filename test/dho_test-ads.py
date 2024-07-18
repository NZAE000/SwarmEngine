from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.advertisement import Advertisements       # Problem to solve
from algorithmSwarm.dho import DHO                                 # Algorithm to use
from util.fitGBest import gBestGraph                               # Show gbest movement
from util.pareto import paretoGraph                                # Show data results


###### MAIN ####################################
try:
  swarm = DHO(Advertisements(), 100, 5)
  swarm.prepare(n_exec=300)
  swarm.solve(n_exec=100)
  swarm.bestToConsole()

  gBestGraph(swarm.path_gbestLog)
  paretoGraph(swarm.path_gbestData)

except Exception as e:
  print(f"{e} \nCaused by {e.__cause__}")