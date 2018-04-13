# This combine qrel CLEF 2016 and 2017. Sorted by Query ID
# consider CLEF 2016 as the primary where duplicates found, judgement from clef2016 will be used
import collections

qrel2016 = "/Volumes/Data/Phd/Data/clef2016_eval/task1.qrels.30Aug"
qrel2017 = "../clef2017_qrels.txt"

qrel2016_2017 = "../clef2016-2017_qrels.txt"

queryDocPairs = {}

#load CLEF 2017 qrels
with open(qrel2017, "r") as fr:
    for line in fr:
        queryId, temp, docId, score = line.strip().split(" ")
        queryDocPairs["{}_{}".format(queryId, docId)] = score
        #print("{} {} {}".format(queryId, docId, score))

#load CLEF 2016 qrels
redundantCount = 0
with open(qrel2016, "r") as fr:
    for line in fr:
        queryId, temp, docId, score = line.strip().split(" ")

        if "{}_{}".format(queryId, docId) in queryDocPairs:
            redundantCount += 1
            print("{}_{}".format(queryId, docId))

        queryDocPairs["{}_{}".format(queryId, docId)] = score


fwRel = open(qrel2016_2017, "w")
for queryDocPair in sorted(queryDocPairs):
    queryId, docId = queryDocPair.split("_")
    fwRel.write("{} 0 {} {}\n".format(queryId, docId, queryDocPairs[queryDocPair]))

fwRel.close()

print("Total Redundant: {}".format(redundantCount))