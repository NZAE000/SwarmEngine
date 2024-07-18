#################################################################################################################################
#################################################################################################################################

This work consists of the implementation of an engine for the optimization of swarm-based metaheuristic algorithms.
Usage:
    - In the folder 'test', are the source files that executing the algorithms with any problems.
        Execution example:  python3.12 test/dho_test-ads.py
    - In the folder 'swarm_logs', are logs of the agents, agent best and movement of the algorithms associated to some problem.
    - In the folder 'data', are the data that the algorithms out when its are prepare to some problem and finishing.

#################################################################################################################################
#################################################################################################################################

# Annotations:
    # Sigmoid mov between -3.5 and 3.5 with constant = -1
    # Therefore, if constan=-0.5, so sigmoid mov between -7 and 7.