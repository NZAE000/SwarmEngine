import matplotlib.pyplot as plt
#from pathlib import Path


def paretoGraph(path_nonDomSolutions, path_allGbest):

## Fill non-dominated solutions.
    file = open(path_nonDomSolutions, "r")
    data = file.readlines()
    y = []
    x = []
    # Fill axis.
    for line in data:
        list_data = line.split("-")
        x.append(int(list_data[1]))
        y.append(int(list_data[0].rstrip("\n")))

## Fill gbest solutions.
    file2 = open(path_allGbest, "r")
    data2 = file2.readlines()

    x2 = []
    y2 = []
    # Fill axis.
    for line in data2:
        list_data = line.split("-")
        x2.append(int(list_data[3]))
        y2.append(int(list_data[2]))

## Create graph.
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', color='b', linestyle='None')
    plt.plot(x2, y2, marker='o', color='r', linestyle='None')


## Adjust the X axis ticks to show a range of numbers.
    #step_x = max(x)/
    #plt.xticks(range(0, max(x), 200))
    #plt.yticks(range(0, max(y), 200))

## Add labels and tittle.
    plt.xlabel('Max')
    plt.ylabel('Min')
    plt.title('Pareto Frontier')
    plt.show()
