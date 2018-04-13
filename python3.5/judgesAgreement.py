# this script evaluate agreement between AMT and CLEF2016 judges.
import csv
import glob
from collections import defaultdict

blockedWorkers = ["A1EF7PCXWNTUXR", "A2SKH7WZUEDGGI", "AH4SMMFHDHK1L", "A1XA2WZVXTTLOI", "A3RYO4RE80IJ84",
                  "A3S104I5V53HB8", "AZ7GSYRVDR23N", "A1XZTIJD9WBHLJ", "A2XYDJS33I2341", "AZZM966F90AL1",
                  "A3B67I3A0YR2D", "A1PLY1H54IPJRB", "A1T1FK3P2N408U", "A2LO2DX6H49IKW", "A1RU9BQLDZ1DSY",
                  "AKATSYE8XLYNL"]

qrel2016 = "/Volumes/Data/Phd/Data/clef2016_eval/task1.qrels.30Aug"

folderInput = "../Results/"

topicRel2017 = {}

print("Loading results from AMT")
for folderName in glob.glob(folderInput + "*"):
    for fileName in glob.glob(folderName + "/*"):
        with open(fileName, newline='') as inputFile:
            csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')
            header = next(csvReader)  # get the header row

            for row in csvReader:
                workerId = row[header.index("WorkerId")]
                status = row[header.index("AssignmentStatus")]

                if workerId not in blockedWorkers and status != "Rejected":
                    queryPrefix = row[header.index("Input.query_prefix")]
                    docId = row[header.index("Input.doc_id")]
                    relScore = row[header.index("Answer.relevance")]

                    topicRel2017["{}_{}".format(queryPrefix, docId)] = {"relScore": relScore, "workerId": workerId}


# load CLEF 2016 qrels to topic relevance 2016
topicRel2016 = {}
redundantCount = 0
allBinRelevantTrue = 0
allBinRelevantFalse = 0
allBinNonRelevantTrue = 0
allBinNonRelevantFalse = 0

allGradedHighRelevantTrue = 0
allGradedHighRelevantFalse = 0
allGradedRelevantTrue = 0
allGradedRelevantFalse = 0
allGradedNonRelevantTrue = 0
allGradedNonRelevantFalse = 0

topicDoc2017 = []
with open(qrel2016, "r") as fr:
    for line in fr:
        queryId, temp, docId, relScore2016 = line.strip().split(" ")
        topicId = queryId[:3]

        if "{}_{}".format(topicId, docId) in topicRel2017 and "{}_{}".format(topicId, docId) not in topicDoc2017:
            topicDoc2017.append("{}_{}".format(topicId, docId))
            redundantCount += 1

            # if 2017: highly relevant
            if topicRel2017["{}_{}".format(topicId, docId)]["relScore"] == "2":
                if relScore2016 == "2":
                    allGradedHighRelevantTrue += 1
                    allBinRelevantTrue += 1

                elif relScore2016 == "1":
                    allGradedHighRelevantFalse += 1
                    allBinRelevantTrue += 1

                elif relScore2016 == "0":
                    allGradedHighRelevantFalse += 1
                    allBinRelevantFalse += 1

            # if 2017: relevant
            if topicRel2017["{}_{}".format(topicId, docId)]["relScore"] == "1":
                if relScore2016 == "2":
                    allGradedRelevantFalse += 1
                    allBinRelevantTrue += 1

                elif relScore2016 == "1":
                    allGradedRelevantTrue += 1
                    allBinRelevantTrue += 1

                elif relScore2016 == "0":
                    allGradedRelevantFalse += 1
                    allBinRelevantFalse += 1

            # if 2017: non relevant
            if topicRel2017["{}_{}".format(topicId, docId)]["relScore"] == "0":
                if relScore2016 == "2":
                    allGradedNonRelevantFalse += 1
                    allBinNonRelevantFalse += 1

                elif relScore2016 == "1":
                    allGradedNonRelevantFalse += 1
                    allBinNonRelevantFalse += 1

                elif relScore2016 == "0":
                    allGradedNonRelevantTrue += 1
                    allBinNonRelevantTrue += 1


print("Total 2017 judgements: {}".format(len(topicRel2017)))
print("Total redundant: {}".format(redundantCount))

print("Binary Relevant True:{}  False:{} \t\t Binary NonRelevant True:{}  False:{}".
      format(allBinRelevantTrue, allBinRelevantFalse, allBinNonRelevantTrue, allBinNonRelevantFalse))

print("% Agreement Binary (true / total redundant): {}%".
      format(((allBinRelevantTrue + allBinNonRelevantTrue) / redundantCount) * 100))

print("% Disagreement Binary (false / total redundant): {}%".
      format(((allBinRelevantFalse + allBinNonRelevantFalse) / redundantCount) * 100))