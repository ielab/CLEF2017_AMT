# Generate Topic details JSON file from CLEF2016_relevantCriteria.csv and topic_clef.json

import json
import csv

fileRelevantCriteria = "/Volumes/Data/Phd/Data/Clef2017_eval/CLEF2016_RelevantCriteria.csv"
fileTopicDescription = "/Volumes/Data/Phd/Data/Clef2017_eval/topics_clef.json"
fileTopicIdQueryPrefix = "/Volumes/Data/Phd/Data/Clef2017_eval/TopicId-QueryPrefix.csv"

outTopicDetails = "/Volumes/Data/Phd/Data/Clef2017_eval/CLEF2016_TopicDetails.json"

dataTopicDescription = json.load(open(fileTopicDescription, "r"))

# intialise and load topic data
topics = {}
for topic in dataTopicDescription:
    topicData = {"title": topic["title"], "description": topic["description"], "criteria": "", "queryPrefix": ""}
    topics[topic["qId"]] = topicData

# load relevant criteria
with open(fileRelevantCriteria, newline='') as fCriteria:
    csvReader = csv.reader(fCriteria)

    next(csvReader) # skip the header

    for line in csvReader:
        topics[line[0]]["criteria"] = line[1]

# load Prefix Query
with open(fileTopicIdQueryPrefix, newline='') as fQueryPrefix:
    csvReader = csv.reader(fQueryPrefix)

    next(csvReader) # skip the header

    for line in csvReader:
        if line[0] not in topics:
            print("Not found: {}".format(line[0]))
        topics[line[0]]["queryPrefix"] = line[1]


# restructure the dictionary to array
jsonData = []
for topicId, data in topics.items():
    topicData = {"topicId": topicId, "title": data["title"], "description": data["description"],
                 "criteria": data["criteria"], "queryPrefix": data["queryPrefix"]}
    jsonData.append(topicData)

# write json data to the output file
with open(outTopicDetails, "w") as fw:
    json.dump(jsonData, fw, indent=4, sort_keys=True)
