import numpy as np
import os

def test(testcases, directory = ""):
    diffSum = 0
    totalNum = 0

    for u in testcases:
        testFile = directory + "u" + str(u) + ".test"
        resultFile = directory + "u" + str(u) + ".base_prediction.txt"

        with open(testFile, 'r') as f:
            lines1 = f.readlines()

        with open(resultFile, 'r') as f:
            lines2 = f.readlines()

        tmp = diffSum
        for i in range(len(lines1)): # user id | item id | rating | timestamp
            _, __, answer, ___ = list(map(int, lines1[i].split()))
            _, __, predict = list(map(int, lines2[i].split()))

            diffSum += (answer - predict) ** 2
        print("#", u, " rmse:", np.sqrt((diffSum - tmp)/len(lines1)))

        totalNum += len(lines1)

    rmse = np.sqrt(diffSum /totalNum)

    return rmse

if __name__ == "__main__":
    testcases = [1,2,3,4,5]
    directory="data-2/"
    
    cmds = ""
    for i in testcases:
        cmds += "python3 recommender.py " + directory + "u" + str(i) + ".base " + directory + "u" + str(i) + ".test\n"

    # testcases = [1,2,3,4,5]
    os.system(cmds)
    print("전체 rmse", test(testcases, directory="data-2/"))