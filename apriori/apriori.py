'''
2017030064 Yoon Hyewon
Programming Assignment 1
'''
import sys
from itertools import combinations
import time

def initFrequentItemset(transaction, minSupportNum):
    counted_items = dict()

    # count numbers of each item
    for trans in transaction:
        for item in trans:
            if item in counted_items:
                counted_items[item] += 1
            else:
                counted_items[item] = 1

    # check frequency
    frequent_itemsets = list()
    frequent_itemsets_count = list()

    for item in counted_items:
        if int(counted_items[item]) >= minSupportNum:
            frequent_itemsets.append([item])
            frequent_itemsets_count.append(int(counted_items[item]))

    return frequent_itemsets, frequent_itemsets_count

def countItemset(transactions, candid_itemsets):
    num_of_candid = len(candid_itemsets)
    count = [0 for i in range(num_of_candid)]

    for trans in transactions:
        i = 0

        for candid in candid_itemsets:
            isContained = True

            for item in candid:
                if item not in trans:
                    isContained = False
                    break
            
            if isContained:
                count[i] += 1
                
            i += 1

    return count

def getFrequentItemset(candid_itemsets, count, minSupportNum):
    frequent_itemsets = list()
    frequent_itemsets_count = list()

    for i in range(len(candid_itemsets)):

        if count[i] >= minSupportNum:
            frequent_itemsets.append(candid_itemsets[i])
            frequent_itemsets_count.append(count[i])

    return frequent_itemsets, frequent_itemsets_count

def makeCandidItemsets(frequent_itemsets):
    candid_itemsets = list()

    # self-joining
    for i in range(len(frequent_itemsets) - 1):
        for j in range(i+1, len(frequent_itemsets)):
            candid = frequent_itemsets[i].copy()

            for item in frequent_itemsets[j]:
                if item not in candid:
                    candid.append(item)

            if len(candid) != len(frequent_itemsets[i]) + 1:
                continue

            # pruning
            isSmallerFrequent = True

            for item in candid:
                smallFreq = candid.copy()
                smallFreq.remove(item)

                if smallFreq not in frequent_itemsets:
                    isSmallerFrequent = False
                    break
            
            if isSmallerFrequent:
                candid_itemsets.append(candid)

    return candid_itemsets

def apriori(transactions, minSupportPercent):
    minSupportNum = len(transactions) * minSupportPercent / 100

    frequent_itemsets, frequent_itemsets_count = initFrequentItemset(transactions, minSupportNum)

    result = frequent_itemsets.copy()
    result_count = frequent_itemsets_count.copy()

    while len(frequent_itemsets) != 0:
        candid_itemsets = makeCandidItemsets(frequent_itemsets)

        # count the number of candidates
        count = countItemset(transactions, candid_itemsets)

        # candidates with minSupport
        frequent_itemsets, frequent_itemsets_count = getFrequentItemset(candid_itemsets, count, minSupportNum)

        # add to result
        result += frequent_itemsets
        result_count += frequent_itemsets_count

    # print(result)
    # print(result_count)

    return result, result_count

def devideItemset(devided_pat, freq_pattern):
    length = len(freq_pattern)
    devided_sets = list()

    for k in range(1, int(length / 2) + 1): #k of nCk
        # nCk
        comb = combinations(freq_pattern, k)

        for tup in comb:
            item_a = set(tup)
            item_b = set(freq_pattern) - item_a

            if (item_a, item_b) not in devided_pat:
                devided_sets.append((item_a, item_b))
                # print((item_a, item_b))

            if k * 2 < length and (item_b, item_a) not in devided_pat:
                devided_sets.append((item_b, item_a))
                # print((item_b, item_a))

    return devided_sets

def getIdxInList(frequent_patterns, itemset):
    idx = -1
    
    for pat in frequent_patterns:
        idx += 1
        if set(pat) == itemset:
            break

    return idx

def calcSupport(transactions, frequent_patterns, counts, itemset_a, itemset_b):
    joined_set = itemset_a.union(itemset_b)

    idx = getIdxInList(frequent_patterns, joined_set)

    if idx == -1:
        count = 0
    else:
        count = counts[idx]

    return round(count / len(transactions) * 100, 2)

def calcConfidence(frequent_patterns, counts, itemset_a, itemset_b):
    joined_set = itemset_a.union(itemset_b)

    idx_a = getIdxInList(frequent_patterns, itemset_a)
    idx_ab = getIdxInList(frequent_patterns, joined_set)

    count_a = counts[idx_a] if idx_a > -1 else 0
    count_ab = counts[idx_ab] if idx_ab > -1 else 0

    percent = count_ab / count_a * 100

    if percent > 100:
        percent = 100

    return round(percent, 2)

def main(minSupportPercent, inputFile, outputFile):
    try:
        transactions = []

        # read input file
        f = open("input.txt", 'r')

        for line in f.readlines():
            line = line.rstrip()
            transactions.append(line.split('\t'))

        f.close()

        frequent_patterns, counts = apriori(transactions, minSupportPercent)

        # write output file
        f = open(outputFile, 'w')

        devided_pat = list()
        for pat in frequent_patterns:
            if len(pat) == 1:
                continue

            devided_pat += devideItemset(devided_pat, pat)

        # write rules to file
        for tup in devided_pat:
            itemset_a, itemset_b = tup # set, set

            row = str(set(map(int, itemset_a))) + "\t" + str(set(map(int, itemset_b))) + "\t"
            row += str(calcSupport(transactions,frequent_patterns, counts, itemset_a, itemset_b)) + "\t"
            row += str(calcConfidence(frequent_patterns, counts, itemset_a, itemset_b)) + "\n"

            f.write(row)

        f.close()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        minSupportPercent = int(sys.argv[1]) # %
        inputFile = sys.argv[2]
        outputFile = sys.argv[3]

        main(minSupportPercent, inputFile, outputFile)

    except Exception as e:
        print(e)