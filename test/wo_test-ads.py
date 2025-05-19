from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.advertisement import Advertisements       # Problem to solve.
from algorithmSwarm.wo import WO                                   # Algorithm to use.
from util.fitGBestPlot import gBestGraph                           # Show gbest movement.
from util.nonDominatedGenerator import nonDomGenerator             # Generate no dominated solutions.
from util.paretoplot import paretoGraph                            # Show data results.


if __name__ == "__main__":
	try:
		swarm = WO(Advertisements(), 100, 22)
		swarm.solve(n_exec=30)
		swarm.bestToConsole()

		gBestGraph(swarm.path_gbestLog)
		path_nonDomSol = nonDomGenerator(swarm.problem)
		paretoGraph(path_nonDomSol, swarm.path_gbestData)

	except Exception as e:
		print(f"{e} \nCaused by {e.__cause__}")