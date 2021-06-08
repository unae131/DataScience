"""
Date : 2021.06.06
GitName : unae131
Recommendation system using CF(Collaborative Filtering) approach
"""
import sys
import time
import numpy as np
from wrmf import *

def fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.5):
    nUsers = len(ratingMatrix)
    nItems = len(ratingMatrix[0])
    ratingMatrix = np.array(ratingMatrix)

    interest = []
    for i in range(nUsers):
        for j in range(nItems):
            if ratingMatrix[i][j] != 0:
                continue
            
            interest.append(binaryMatrix[i][j])

    interest.sort()

    maxUninterest = interest[int(theta * len(interest))]
    
    for i in range(nUsers):
        for j in range(nItems):
            if ratingMatrix[i][j] != 0:
                continue
        
            if binaryMatrix[i][j] > maxUninterest:
                ratingMatrix[i][j] = 3

            else:
                ratingMatrix[i][j] = 2
            
    return ratingMatrix

def inferPreUsePrefer(binaryMatrix): # svd
    u, s, vh = np.linalg.svd(binaryMatrix, full_matrices=False)
    us = np.matmul(u, np.diag(s))
    inferedBinaryMatrix = np.matmul(us, vh)
    return inferedBinaryMatrix

def _getRatingMatrix(dataset):
    users = list(dataset.keys())
    users.sort()
    userIDs = dict()
    i = 0
    for id in users:
        userIDs[id] = i
        i+=1

    items = set()
    for user in users:
        for item in list(dataset[user].keys()):
            items.add(item)
    items = list(items)
    items.sort()
    itemIDs = dict()
    i = 0
    for id in items:
        itemIDs[id] = i
        i+=1

    ratingMatrix = np.full((len(users), len(items)), 0, dtype = np.uint8)
    binaryMatrix = np.full((len(users), len(items)), 0., dtype = np.float64)
    i = 0
    for user in users:
        j = 0
        for item in items:
            if item in dataset[user]:
                ratingMatrix[i][j] = dataset[user][item]
                binaryMatrix[i][j] = 1.
            j += 1
        i += 1

    return userIDs, itemIDs, ratingMatrix, binaryMatrix

def readInputFile(trainFile):
    with open(trainFile, 'r') as f:
        lines = f.readlines()

    dataset = dict()
    
    for line in lines: # user id | item id | rating | timestamp
        user, item, rating, _ = list(map(int, line.split()))

        if user not in dataset:
            dataset[user] = dict()

        dataset[user][item] = rating

    return _getRatingMatrix(dataset)

def writeOutputFile(testFileName, ratingMatrix, userIDs, itemIDs):
    with open(testFileName, 'r') as f:
        lines = f.readlines()

    result = ""

    for line in lines: # user id | item id | rating | timestamp
        user, item, __, __ = list(map(int, line.split()))

        try:
            rating = ratingMatrix[userIDs[user]][itemIDs[item]]
        except KeyError:
            rating = 3

        result += str(user) + "\t" + str(item) + "\t" + str(rating) + "\n"

    resultFileName = testFileName.split(".")[0]+".base_prediction.txt"
    with open(resultFileName, 'w') as f:
        f.write(result)
    
    return resultFileName

def testRMSE(testFile):
    with open(testFile, 'r') as f:
        lines1 = f.readlines()

    resultFile = testFile.split(".")[0] + ".base_prediction.txt"
    with open(resultFile, 'r') as f:
        lines2 = f.readlines()

    diffSum = 0
    for i in range(len(lines1)): # user id | item id | rating | timestamp
        __, __, answer, __ = list(map(int, lines1[i].split()))
        __, __, predict = list(map(int, lines2[i].split()))

        diffSum += (answer - predict) ** 2

    rmse = np.sqrt(diffSum / len(lines1))
    return rmse

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Insufficient arguments!")
        print("\"recommender.py [train data file name] [test data file name]\"")
    
    else:
        startTime = time.time()

        userIDs, itemIDs, ratingMatrix, binaryMatrix = readInputFile(sys.argv[1])
        binaryMatrix = inferPreUsePrefer(ratingMatrix)
        ratingMatrix = fillRatingMatrix(ratingMatrix, binaryMatrix)

        writeOutputFile(sys.argv[2], ratingMatrix, userIDs, itemIDs)
        
        finishTime = time.time()
        print(sys.argv[1], finishTime - startTime, "초")
        print("rmse", testRMSE(sys.argv[2]))
