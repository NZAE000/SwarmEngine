import matplotlib.pyplot as plt


def gBestGraph(path):

    file = open(path,"r")
    data = file.readlines()

    x = []
    y = []

    # Fill axis
    count = 0
    for line in data:
        list_data = line.split("-")
        x.append(count)
        y.append(float(list_data[0]))
        count += 1

    # Create graph
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', color='b')


    # Adjust the X axis ticks to show a range of numbers
    #plt.xticks(range(0, max(x), 300 ))  # Muestra cada 10º valor en el eje X
    #plt.yticks(range(0, max(y), 500))  # Muestra cada 10º valor en el eje X

    # Add labels and tittle
    plt.xlabel('Interations')
    plt.ylabel('Fit-GBest')
    plt.title('GBest movement')

    plt.show()