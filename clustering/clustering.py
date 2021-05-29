"""
Date : 2021.05.29
GitName : unae131
DBSCAN Clustering for DataScience Class
"""
import sys
import math
import time

def dbscan(dataset, eps, minpts): # data : id, x_coord, y_coord, processed
    n = 1
    for data in dataset:
        if data[3] > 0: # processed data
            continue
        
        n = retrieveDensityReachable(dataset, data, eps, minpts, n)
    
    return n - 1

def retrieveDensityReachable(dataset, p, eps, minpts, cluster_id):
    neighbors = getNeighbors(dataset, p, eps)

    if len(neighbors) < minpts: # outlier
        return cluster_id

    # core point
    p[3] = cluster_id
    while True:
        if len(neighbors) == 0: # all of the points have been processed
            break
        
        neighbor_neighbors = []
        for neighbor in neighbors:

            if neighbor[3] > 0: # processed
                continue

            neighbor[3] = cluster_id
            new_neighbors = getNeighbors(dataset, neighbor, eps)

            if len(new_neighbors) >= minpts: # it's not a border point
                neighbor_neighbors += new_neighbors

        neighbors = neighbor_neighbors
    
    return cluster_id + 1

def getNeighbors(dataset, p, eps):
    neighbors = []
    for data in dataset:
        if distance(p, data) <= eps:
            neighbors.append(data)

    return neighbors

def distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

def selectClusters(dataset, n):
    clusters = {}

    for data in dataset:
        if data[3] not in clusters:
            clusters[data[3]] = [data]
            continue

        clusters[data[3]].append(data)

    del(clusters[0]) # remove outliers

    if len(clusters) < n:
        for i in range(n - len(clusters)):
            clusters[-i] = []
        return clusters

    if len(clusters) == n:
        return clusters
    
    # remove small (n - len(clusters)) clusters
    removeNum = len(clusters) - n
    for i in range(removeNum):
        minId = -1
        minLen = 0

        for id in clusters:
            if minId == -1:
                minId = id
                minLen = len(clusters[id])
                continue

            newLen = len(clusters[id])
            
            if newLen < minLen:
                minId = id
                minLen = newLen

        del(clusters[minId])

    return clusters

def readInputFile(fileName):
    with open(fileName, 'r') as f:
        lines = f.readlines()

    dataset = []

    for line in lines:
        dataset.append(list(map(float, line.split())) + [0.])
    
    return dataset

def writeOutputFile(inputFileName, clusters):
    i = 0
    for id in clusters:
        result = ""

        for data in clusters[id]:
            result += str(int(data[0])) + "\n"

        outputFileName = inputFileName[:-4] + "_cluster_" + str(i) +".txt"

        with open(outputFileName, 'w') as f:
            f.write(result)

        i += 1

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Insufficient arguments!")
        print("\"clustering.py [input data file name] [# of clusters] [Eps] [MinPts]\"")

    startTime = time.time()

    dataset = readInputFile(sys.argv[1])
    numCluster = int(sys.argv[2])
    eps = float(sys.argv[3])
    minpts = int(sys.argv[4])
    
    n = dbscan(dataset, eps, minpts)
    clusters = selectClusters(dataset, numCluster)

    print("# of clusters : ", n)
    print("select ", numCluster)
    for c in clusters:
        print(c, " : ", len(clusters[c]))

    writeOutputFile(sys.argv[1], clusters)

    finishTime = time.time()
    print(finishTime - startTime, " 초 경과")