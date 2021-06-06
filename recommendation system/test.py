import numpy as np

def test(directory = "", num = 5):
    diffSum = 0
    totalNum = 0

    for u in range(1, num+1):
        testFile = directory + "u" + str(u) + ".test"
        resultFile = directory + "u" + str(u) + ".base_prediction.txt"

        with open(testFile, 'r') as f:
            lines1 = f.readlines()

        with open(resultFile, 'r') as f:
            lines2 = f.readlines()

        for i in range(len(lines1)): # user id | item id | rating | timestamp
            _, __, answer, ___ = list(map(int, lines1[i].split()))
            _, __, predict = list(map(int, lines2[i].split()))

            diffSum += (answer - predict) ** 2
        
        totalNum += len(lines1)

    rmse = np.sqrt(diffSum /totalNum)

    return rmse

print(test(directory="data-2/"))