from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.advertisement import Advertisements       # Problem to solve
from algorithmSwarm.wo import WO                                   # Algorithm to use
from util.fitGBestPlot import gBestGraph                           # Show gbest movement
from util.pareto import paretoGraph                                # Show data results


###### MAIN ####################################
try:
  swarm = WO(Advertisements(), 100, 22)
  swarm.prepare(n_exec=50)
  print("SOLVE")
  swarm.solve(n_exec=30)
  swarm.bestToConsole()

  gBestGraph(swarm.path_gbestLog)
  paretoGraph(swarm.path_gbestData)

except Exception as e:
  print(f"{e} \nCaused by {e.__cause__}")