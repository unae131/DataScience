"""
Name : 윤혜원
Recommendation system using CF(Collaborative Filtering) approach
"""
import sys
import time
import numpy as np

def getMean(ratings):
    count = 0
    for i in range(len(ratings)):

        if ratings[i] == 0:
            continue

        count += 1

    mean = np.sum(ratings) / count
    return mean

def aggregateRatings(ratingMatrix, K):
    nUsers = len(ratingMatrix)
    nItems = len(ratingMatrix[0])
    userMeans = []
    similarities = dict()
    w = []

    for i in range(nUsers):
        userMeans.append(getMean(ratingMatrix[i]))
        similarities[i] = dict()
        w.append(ratingMatrix[i] / np.sqrt(np.sum(ratingMatrix[i] * ratingMatrix[i])))

    # get cosine similarity
    for i in range(1, nUsers):
        for j in range(i, nUsers):
            similarities[i][j] = np.sum(w[i]*w[j])
            similarities[j][i] = similarities[i][j]

    # find k neighbors
    neighbors = []    
    for i in range(nUsers):
        neighbors.append(dict(sorted(similarities[i].items(), reverse=True, key = lambda item : item[1])))

    # aggregate
    for i in range(nUsers):
        for j in range(nItems):
            if ratingMatrix[i][j] != 0:
                continue

            k = 0
            wSum = 0
            for userIdx in neighbors[i]:
                if k >= K:
                    break

                if i == userIdx or ratingMatrix[userIdx][j] == 0:
                    continue

                wSum += neighbors[i][userIdx] * (ratingMatrix[userIdx][j] - userMeans[userIdx])
                k+=1

            predicted = round(userMeans[i] + 1.957 / (K) * wSum)
            
            if predicted < 1:
                predicted = 1

            elif predicted > 5:
                predicted = 5

            ratingMatrix[i][j] = predicted

    return ratingMatrix, userMeans

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

def writeOutputFile(testFileName, ratingMatrix, userIDs, itemIDs, userMeans, itemMeans):
    with open(testFileName, 'r') as f:
        lines = f.readlines()

    result = ""

    for line in lines: # user id | item id | rating | timestamp
        user, item, __, __ = list(map(int, line.split()))

        if user not in userIDs and item not in itemIDs:
            rating = round(np.sum(userMeans) / len(userMeans))
        elif user not in userIDs:
            rating = round(itemMeans[itemIDs[item]])
        elif item not in itemIDs:
            rating = round(userMeans[userIDs[user]])
        else:
            rating = ratingMatrix[userIDs[user]][itemIDs[item]]

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
        ratingMatrix, userMeans = aggregateRatings(ratingMatrix, 10)

        itemMeans = []
        for i in range(len(itemIDs)):
            itemMeans.append(ratingMatrix[:,i])

        writeOutputFile(sys.argv[2], ratingMatrix, userIDs, itemIDs, userMeans, itemMeans)
        
        finishTime = time.time()
        print(sys.argv[1], finishTime - startTime, "초")
