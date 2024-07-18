import statistics

def getMedianMinMax(path):
    all_minmaxs = []

    with open(path, 'r') as fileReaer:
        line = fileReaer.readline()
        # Cast to int and store in list of lists of lists
        while line:
            minmaxs_prev = line.strip("[]\n").split("], [")
            minmaxs = []
            for minmax in minmaxs_prev:
                minmaxs.append([ float(value) for value in minmax.split(",") ])

            all_minmaxs.append(minmaxs)
            line = fileReaer.readline()
    
# Initialize all_minmaxs_join according to the size of an element
    all_minmaxs_join = []
    size1 = len(all_minmaxs[0])
    size2 = len(all_minmaxs[0][0])

    for i in range(size1): # Initialize all_minmaxs_join according to the size of an element
        lista = []
        for j in range(size2):
            lista.append([])
        all_minmaxs_join.append(lista)

    #print(all_minmaxs_join) # -> [[[], []], [[], []], [[], []], [[], []], [[], []]]

# Join min and max  -> [[[4,3,4,5, ..], [1,4,5,6,7, ..]], [[..], [..]], [[..], [..]], [[..], [..]], [[..], [..]]]
    for minmaxs in all_minmaxs:
        for i in range(size1):
            for j in range(size2):
                all_minmaxs_join[i][j].append(minmaxs[i][j])

# Calcule median to min and max
    median_minmax = []
    for i in range(size1):
        median_minmax.append([])
        #median_minmax[i].append(min(all_minmaxs_join[i][0]))
        #median_minmax[i].append(max(all_minmaxs_join[i][1]))
        for j in range(size2):
            median_minmax[i].append(statistics.mean(all_minmaxs_join[i][j]))
        #    #all_minmaxs_join[i][j].sort(reverse=True)

    return median_minmax


def displacement(minmaxs):
    minmaxs_disp = []
    for minmax in minmaxs:
        min = abs(minmax[0])
        max = abs(minmax[1])
        media = (min + max) / 2
        minmaxs_disp.append([-media, media])
    return minmaxs_disp
# 3.5 = 1 
# 7   = x
#
# Sigmoid mov between -3.5 and 3.5 with constant = -1
# Therefore, if constant=-0.5, so sigmoid mov between -7 and 7
def getConstants(minmaxs):
    constants = []
    for minmax in minmaxs:
        constant = 3.5/minmax[1]
        constants.append(constant)
    return constants

## MAIN ###############################################################   

#median_minmaxs = getMedianMinMax("data/minmax_movPSO-ads.txt")
#print(median_minmaxs)
#median_minmaxs_disp = displacement(median_minmaxs)
#print(median_minmaxs_disp)
#print(getConstants(median_minmaxs_disp))