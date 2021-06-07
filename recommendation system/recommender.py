"""
Date : 2021.06.06
GitName : unae131
Recommendation system using CF(Collaborative Filtering) approach
"""
import sys
import time
import numpy as np

def loss(binaryMatrix, U, V, C, r_lambda):
    return np.sum(C * (binaryMatrix - (U @ V.T) ** 2)) + r_lambda * (np.sum(U*U) + np.sum(V*V)) 

def update(binaryMatrix, nUsers, nItems, nFactor, U, V, C, r_lambda):
    lambdaI = r_lambda * np.eye(nFactor)

    for u in range(nUsers):
        Cu = np.diag(C[u])
        U[u] = np.linalg.inv(V.T @ Cu @ V + lambdaI) @ V.T @ Cu @ binaryMatrix[u]

    for i in range(nItems):
        Ci = np.diag(C[:, i])
        V[i] = np.linalg.inv(U.T @ Ci @ U + lambdaI) @ U.T @ Ci @ binaryMatrix[:, i]

    return U, V

def als(binaryMatrix, r_lambda = 150, nFactor = 100, alpha = 40, epoch = 10):
    nUsers = len(binaryMatrix)
    nItems = len(binaryMatrix[0])

    # initialize U and V
    U = np.random.rand(nUsers, nFactor) * 0.16
    V = np.random.rand(nItems, nFactor) * 0.16
    C = 1 + alpha * binaryMatrix

    # loss
    for k in range(epoch):
        print(loss(binaryMatrix, U, V, C, r_lambda))
        U, V = update(binaryMatrix, nUsers, nItems, nFactor, U, V, C, r_lambda)

    return U @ V.T

def fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.5):
    nUsers = len(ratingMatrix)
    nItems = len(ratingMatrix[0])

    for i in range(nUsers):
        for j in range(nItems):
            if ratingMatrix[i][j] != 0:
                continue
            
            if binaryMatrix[i][j] > theta:
                ratingMatrix[i][j] = 3

            else:
                ratingMatrix[i][j] = 2

    return ratingMatrix

def inferPreUsePrefer(binaryMatrix): # svd
    u, s, vh = np.linalg.svd(binaryMatrix, full_matrices=False)
    us = np.matmul(u, np.diag(s))
    inferedBinaryMatrix = np.matmul(us, vh)
    return inferedBinaryMatrix

def getRatingMatrix(dataset):
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
                ratingMatrix[i][j] = dataset[user][item][0]
                binaryMatrix[i][j] = 1.
            j += 1
        i += 1

    return userIDs, itemIDs, ratingMatrix, binaryMatrix

def readInputFile(trainFile, testFile):
    with open(trainFile, 'r') as f:
        lines = f.readlines()

    dataset = dict()
    
    for line in lines: # user id | item id | rating | timestamp
        user, item, rating, timestamp = list(map(int, line.split()))

        if user not in dataset:
            dataset[user] = dict()

        dataset[user][item] = [rating, timestamp]

    # test file
    with open(testFile, 'r') as f:
        lines = f.readlines()

    for line in lines: # user id | item id | rating | timestamp
        user, item, _, __ = list(map(int, line.split()))

        if user not in dataset:
            dataset[user] = dict()

        dataset[user][item] = [0, 0]

    return dataset

def writeOutputFile(testFileName, ratingMatrix, userIDs, itemIDs):
    with open(testFileName, 'r') as f:
        lines = f.readlines()

    result = ""

    for line in lines: # user id | item id | rating | timestamp
        user, item, _, __ = list(map(int, line.split()))

        result += str(user) + "\t" + str(item) + "\t" + str(ratingMatrix[userIDs[user]][itemIDs[item]]) + "\n"

    resultFileName = testFileName.split(".")[0]+".base_prediction.txt"
    with open(resultFileName, 'w') as f:
        f.write(result)
    
    return resultFileName

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Insufficient arguments!")
        print("\"recommender.py [train data file name] [test data file name]\"")
    
    else:
        startTime = time.time()

        dataset = readInputFile(sys.argv[1], sys.argv[2])
        # print(dataset)

        userIDs, itemIDs, ratingMatrix, binaryMatrix = getRatingMatrix(dataset)
        # binaryMatrix = inferPreUsePrefer(binaryMatrix)
        binaryMatrix = als(binaryMatrix)
        ratingMatrix = fillRatingMatrix(ratingMatrix, binaryMatrix)
        writeOutputFile(sys.argv[2], ratingMatrix, userIDs, itemIDs)

        finishTime = time.time()
        print(sys.argv[1], finishTime - startTime, "초")
