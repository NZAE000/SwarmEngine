import matplotlib.pyplot as plt
from pathlib import Path


def paretoGraph(path):

## Fill non-dominated solutions
    file = open(str(Path(__file__).parent) + "/non-dominated_solutions_ads.txt","r")
    data = file.readlines()

    y = []
    x = []
    # Fill axis
    for line in data:
        list_data = line.split(",")
        x.append(int(list_data[0]))
        y.append(int(list_data[1].rstrip("\n")))

## Fill gbest solutions
    file2 = open(path,"r")
    data2 = file2.readlines()

    x2 = []
    y2 = []
    # Fill axis
    for line in data2:
        list_data = line.split("-")
        x2.append(int(list_data[3]))
        y2.append(int(list_data[2]))

# Create graph
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', color='b', linestyle='None')
    plt.plot(x2, y2, marker='o', color='r', linestyle='None')


# Adjust the X axis ticks to show a range of numbers
    plt.xticks(range(0, max(x), 300 ))
    plt.yticks(range(0, max(y), 500))

# Add labels and tittle
    plt.xlabel('Max')
    plt.ylabel('Min')
    plt.title('Pareto Frontier')

    plt.show()
