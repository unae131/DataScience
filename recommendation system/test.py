import numpy as np
import os

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

if __name__ == "__main__":
    testcases = 5
    directory="data-2/"
    
    cmds = ""
    for i in range(1, testcases + 1):
        cmds += "python3 recommender.py " + directory + "u" + str(i) + ".base " + directory + "u" + str(i) + ".test\n"

    os.system(cmds)
    print("전체 rmse", test(directory="data-2/", num= testcases))