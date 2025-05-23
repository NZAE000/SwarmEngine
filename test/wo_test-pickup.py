from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.pickup import Pickup                      # Problem to solve.
from algorithmSwarm.wo import WO                                   # Algorithm to use.
from util.fitGBestPlot import gBestGraph                           # Show gbest movement.
from util.statistics import showMetrics							   # Show staditics.
from util.nonDominatedGenerator import nonDomGenerator             # Generate no dominated solutions.
from util.paretoplot import paretoGraph                            # Show data results.


if __name__ == "__main__":
	try:
		swarm = WO(Pickup(), 200, 44) # 500, 46
		swarm.solve(n_exec=30, measure_time=False)
		swarm.bestToConsole()

		gBestGraph(swarm.path_gbestLog)
		showMetrics(swarm.path_execTimeData, swarm.path_gbestData)
		#path_nonDomSol = nonDomGenerator(swarm.problem)
		#paretoGraph(path_nonDomSol, swarm.path_gbestData)

	except Exception as e:
		print(f"{e} \nCaused by {e.__cause__}")