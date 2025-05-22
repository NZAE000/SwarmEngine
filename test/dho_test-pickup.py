from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.pickup import Pickup                      # Problem to solve
from algorithmSwarm.dho import DHO                                 # Algorithm to use
from util.fitGBestPlot import gBestGraph                           # Show gbest movement
from util.nonDominatedGenerator import nonDomGenerator             # Generate no dominated solutions
from util.paretoplot import paretoGraph                            # Show data results on pareto frontier


if __name__ == "__main__":
    try:
        swarm = DHO(Pickup(), 100, 22)
        swarm.solve(n_exec=10, measure_time=True)
        swarm.bestToConsole()

        gBestGraph(swarm.path_gbestLog)
        path_nondom_sol = nonDomGenerator(swarm.problem)
        paretoGraph(path_nondom_sol, swarm.path_gbestData)

    except Exception as e:
        print(f"{e} \nCaused by {e.__cause__}")