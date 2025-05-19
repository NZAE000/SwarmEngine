from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from problemOptimization.backpack import Backpack       # Problem to solve
from algorithmSwarm.wo import WO                        # Algorithm to use


if __name__ == "__main__":
	try:
		swarm = WO(Backpack(), 50, 22)
		swarm.solve(n_exec=30)
		swarm.bestToConsole()

	except Exception as e:
		print(f"{e} \nCaused by {e.__cause__}")