# Generate 50 batch data files. one file for each topic.

import json
from collections import defaultdict

topicDetails = "/Volumes/Data/Phd/Data/Clef2017_eval/CLEF2016_TopicDetails.json"
poolFile = "/Volumes/Data/Phd/Data/Clef2017_eval/pool2017.relevation"

outBatchDataPrefix = "/Volumes/Data/Github/CLEF2017_AMT/AMT_BatchData/batchData_clef2017_"

# load Topic Detail
dataTopicDetail = json.load(open(topicDetails, "r"))

# intialise and load topic data
topics = {}
for topic in dataTopicDetail:
    topicData = {"title": topic["title"], "description": topic["description"], "criteria": topic["criteria"],
                 "topicId": topic["topicId"]}
    topics[topic["queryPrefix"]] = topicData

# load pool
pool = defaultdict(list)
with open(poolFile, 'r') as fPool:
    for line in fPool:
        queryPrefix, t1, docId, t2, t3, t4 = line.split('\t')
        pool[queryPrefix].append(docId)


# write batch data files
for queryPrefix, data in topics.items():
    with open(outBatchDataPrefix + queryPrefix + ".csv", "w") as fw:
        fw.write('query_prefix,topic_id,title,criteria,doc_id\n')
        for docs in pool[queryPrefix]:
            title = data["title"].replace('"', "'")
            criteria = data["criteria"].replace('"', "'")
            fw.write('{},{},"{}","{}",{}\n'.format(queryPrefix, data["topicId"], title, criteria, docs))

    print(queryPrefix)

