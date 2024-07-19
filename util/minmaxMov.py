import math

def getMinMax(path, dimension):
    min    =  math.inf
    max    = -math.inf
    minmax = []
    for i in range(dimension):
        minmax.append([min, max])

    with open(path, 'r') as fileReaer:
        line = fileReaer.readline()
        while line:
            movement = [ float(value) for value in line.strip("[]\n").split(",") ]
            #print(movement)
            

            for j in range(dimension):
                mov = movement[j]
                if mov < minmax[j][0]:     # Set min
                    minmax[j][0] = mov
                elif mov > minmax[j][1]:   # Or set max
                    minmax[j][1] = mov

            line = fileReaer.readline()
    
    return minmax

#minmaxMovement = getMinMax("../swarm_logs/mov_logPSO-ads.txt", 5)
##minmaxMovement = getMinMax("swarm_logs/mov_logDHO-ads.txt", 5)
#print(minmaxMovement)