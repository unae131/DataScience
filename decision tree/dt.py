"""
Date : 2021.04.14
GitName : unae131
Decision Tree for DataScience Class
"""
""" 추가할 것
1. gini measure
2. 상황에 따라 measure 다르게 사용
3. 23개 이상의 트리 노드 수를 가질 경우 프루닝
4. measure 값들 비교 중 동일한 값 있을 때
"""
import numpy as np
import sys
import random
from Node import*

def parseDataSet(filename):
    f = open(filename, "r")
    attr_names = f.readline().strip().split("\t")
    lines = f.readlines()
    
    samples = []
    attr_ranges = {attr : [] for attr in attr_names}

    for line in lines:
        values = line.strip().split("\t")
        
        # check missing value
        if len(values) != len(attr_names):
            continue

        sample = {}
        for i in range(len(attr_names)):
            sample[attr_names[i]] = values[i]

            if values[i] not in attr_ranges[attr_names[i]]:
                attr_ranges[attr_names[i]].append(values[i])

        samples.append(sample)

    f.close()

    return attr_names, samples, attr_ranges

def splitSamples(samples, validRatio):
    num_of_valid = int(len(samples) * validRatio)

    validSamples = []

    for i in range(num_of_valid):
        j = random.randint(0, len(samples) - 1)
        validSamples.append(samples[j])
        del samples[j]

    return samples, validSamples

def makeDecisionTree(samples, attr_names, attr_ranges, measure):
    test_attr, splited = measure(samples, attr_names)

    root = Node(test_attr)
    root.setBranches(splited, attr_ranges[test_attr])
    attr_names.remove(test_attr)

    nodeTuples = [[root, splited, attr_names]]

    for nt in nodeTuples:
        node, splited, attr_names = nt

        totalSamples = []
        for value in splited:
            totalSamples += splited[value]
        majority = voteMajority(split(totalSamples, attr_names[-1]))

        for value in attr_ranges[node.name]:
            # Stop when there's no sample with 'value'
            if value not in splited:
                Node(majority, node, value)
                continue

            samples = splited[value]

            labeledSamples = split(samples, attr_names[-1])

            # Stop when all samples have the same label
            if len(labeledSamples) == 1:
                label = samples[0][attr_names[-1]]
                Node(label, node, value)
                continue
                
            # Stop when there is no spliting attribute to use
            if len(attr_names) == 1:
                label = voteMajority(labeledSamples)
                Node(label, node, value)
                continue
            
            # select a spliting attribute and make a new node with it
            test_attr, newSplited = measure(samples, attr_names)
            newNode = Node(test_attr, node, value)
            newNode.setBranches(newSplited, attr_ranges[test_attr])
            
            newAttr_names = attr_names.copy()
            newAttr_names.remove(test_attr)

            nodeTuples.append([newNode, newSplited, newAttr_names])

    return root

def voteMajority(splited):
    maxCount = -1
    major = ""

    for label in splited:
        if maxCount < len(splited[label]) :
            maxCount = len(splited[label])
            major = label

    return major

def split(samples, attr_name):
    splited = {}
    for sample in samples:
        value = sample[attr_name]

        if value not in splited:
            splited[value] = [sample]
        else:
            splited[value].append(sample)

    return splited

def getInfo(samples, label_name):
    labels = split(samples, label_name)
    len_samples = len(samples)

    info = 0.0
    for l in labels:
        p = len(labels[l]) / len_samples
        info -= p * np.log2(p)

    return info

def getInfoA(len_samples, groups, label_name):
    infoA = 0.0

    for group in groups:
        infoA += len(group)/len_samples * getInfo(group, label_name)

    return infoA

def getSplitInfoA(len_samples, groups):
    splitInfoA = 0.0
    
    for group in groups:
        splitInfoA -= len(group)/len_samples * np.log2(len(group)/len_samples)

    return splitInfoA

def getMaxGainAttr(samples, attr_names):
    info = getInfo(samples, attr_names[-1])
    len_samples = len(samples)

    maxGain = -1
    maxAttr = ""
    maxSplited = None

    for attr in attr_names[:-1]:
        splited = split(samples, attr)
        groups = list(splited.values())

        gainA = info - getInfoA(len_samples, groups, attr_names[-1])

        if gainA > maxGain: # When values are equal, choose first one.
            maxGain = gainA
            maxAttr = attr
            maxSplited = splited

    return maxAttr, maxSplited
        
def getMaxGainRatioAttr(samples, attr_names):
    info = getInfo(samples, attr_names[-1])
    len_samples = len(samples)

    maxGainRatio = -1
    maxAttr = ""
    maxSplited = None

    for attr in attr_names[:-1]:
        splited = split(samples, attr)
        groups = list(splited.values())

        gainA = info - getInfoA(len_samples, groups, attr_names[-1])
        splitInfoA = getSplitInfoA(len_samples, groups)

        if splitInfoA == 0:
            return attr, splited
        
        gainRatio = gainA / splitInfoA
        
        if gainRatio > maxGainRatio: # When values are equal, choose first one.
            maxGainRatio = gainRatio
            maxAttr = attr
            maxSplited = splited

    return maxAttr, maxSplited

def test(samples, dt):
    result = []

    for sample in samples:
        node = dt

        while node.isLeaf != True:
            value = sample[node.name]
            node = node.branches[value]

        result.append(node.name)

    return result

def postPruning(node, samples, label_name):
    if node.isLeaf == True:
        return
    
    splited = split(samples, node.name)
    labeled = split(samples, label_name)
    major_value = voteMajority(labeled)

    major_answer = len(labeled[major_value])
    splited_answer = 0

    for branch_value in splited:
        postPruning(node.branches[branch_value], splited[branch_value], label_name)

        result = test(splited[branch_value], node)

        for i in range(len(result)):
            if result[i] == splited[branch_value][i][label_name]:
                splited_answer += 1

    if major_answer > splited_answer:
        node.deleteBranches(major_value)

def makeResultFile(filename, samples, result, attr_names):
    output = ""

    for attr in attr_names:
        output += attr + "\t"

    output = output[:-1] + "\n"

    i = 0
    for sample in samples:
        for attr in attr_names[:-1]:
            output += sample[attr] + "\t"
        output += result[i] + "\n"
        i+=1

    f = open(filename, "w")
    f.write(output)
    f.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Insufficient arguments!")

    else:
        attr_names, trainSamples, attr_ranges = parseDataSet(sys.argv[1])
        measure = getMaxGainRatioAttr
        pruning = True

        # count available # of nodes
        # node_num = 0
        # for values in attr_ranges.values():
        #     node_num += len(values)
        # print(node_num)

        # if node_num >= 25:
        if pruning == True:
            trainSamples, validSamples = splitSamples(trainSamples, 0.3)

        dt = makeDecisionTree(trainSamples, attr_names.copy(), attr_ranges, measure)

        # if node_num >= 25:
        if pruning == True:
            postPruning(dt, validSamples, attr_names[-1])

        # dt.print("")
        # print(dt.countNode())

        testSamples = parseDataSet(sys.argv[2])[1]
        
        result = test(testSamples, dt)
        
        makeResultFile(sys.argv[3], testSamples, result, attr_names)