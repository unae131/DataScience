"""
Date : 2021.06.06
GitName : unae131
Recommendation system using CF(Collaborative Filtering) approach
"""
import sys
import time
import numpy as np
from wrmf import *

def fillRatingMatrix(ratingMatrix):
    nUsers = len(ratingMatrix)
    nItems = len(ratingMatrix[0])
    ratingMatrix = np.array(ratingMatrix)

    for i in range(nUsers):
        for j in range(nItems):
            if ratingMatrix[i][j] != 0:
                continue
        
            ratingMatrix[i][j] = 3
            
    return ratingMatrix

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
    i = 0
    for user in users:
        j = 0
        for item in items:
            if item in dataset[user]:
                ratingMatrix[i][j] = dataset[user][item]
            j += 1
        i += 1

    return userIDs, itemIDs, ratingMatrix

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

def writeOutputFile(testFileName, ratingMatrix, userIDs, itemIDs, default):
    with open(testFileName, 'r') as f:
        lines = f.readlines()

    result = ""

    for line in lines: # user id | item id | rating | timestamp
        user, item, __, __ = list(map(int, line.split()))

        try:
            rating = ratingMatrix[userIDs[user]][itemIDs[item]]
        except KeyError:
            rating = round(default)

        result += str(user) + "\t" + str(item) + "\t" + str(rating) + "\n"

    resultFileName = testFileName.split(".")[0]+".base_prediction.txt"
    with open(resultFileName, 'w') as f:
        f.write(result)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Insufficient arguments!")
        print("\"recommender.py [train data file name] [test data file name]\"")
    
    else:
        startTime = time.time()

        userIDs, itemIDs, ratingMatrix = readInputFile(sys.argv[1])
        ratingMatrix = fillRatingMatrix(ratingMatrix)

        mean = np.sum(ratingMatrix) / (len(userIDs) * len(itemIDs))
        writeOutputFile(sys.argv[2], ratingMatrix, userIDs, itemIDs, mean)
        
        finishTime = time.time()
        print(sys.argv[1], finishTime - startTime, "초")
