# Get list of already approved assignments from the black listed workers
# output as batch revision to be reuploaded

import csv
import glob
from collections import defaultdict

folderInput = "../Results/2018-04-05/"
blockedWorkers = ["A1EF7PCXWNTUXR", "A2SKH7WZUEDGGI", "AH4SMMFHDHK1L", "A1XA2WZVXTTLOI", "A3RYO4RE80IJ84",
                  "A3S104I5V53HB8", "AZ7GSYRVDR23N", "A1XZTIJD9WBHLJ", "A2XYDJS33I2341", "AZZM966F90AL1",
                  "A3B67I3A0YR2D", "A1PLY1H54IPJRB", "A1T1FK3P2N408U", "A2LO2DX6H49IKW", "A1RU9BQLDZ1DSY",
                  "AKATSYE8XLYNL"]

outputFile = "../AMT_approvedBlackListed/2018-04-05.csv"
outputBatchFolder = "../AMT_BatchData_Revision/"

fw = open(outputFile, 'w', newline='')
csvWriter = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

countApproved = 0
batchData = defaultdict(list)

for filename in glob.glob(folderInput + "*"):
    with open(filename, newline='') as inputFile:
        csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')
        header = next(csvReader)  #get the header row

        for row in csvReader:
            workerId = row[15]
            status = row[16]



            if workerId in blockedWorkers and status == "Approved":
                # write header once
                if countApproved == 0:
                    csvWriter.writerow(header)

                countApproved += 1
                # write only the approved row
                csvWriter.writerow(row)

                queryPrefix = row[27]
                topicId = row[28]
                title = row[29]
                criteria = row[30]
                doc_id = row[31]

                batchData[queryPrefix].append(
                    {"topicId": topicId, "title": title, "criteria": criteria, "doc_id": doc_id})
    print("Finished: {}".format(filename))
print("Count Approved: {}".format(countApproved))
fw.close()

print("Start: generating revision batch data")
for queryPrefix in batchData:
    fw = open(outputBatchFolder + "revisionData_clef2017_" + queryPrefix + ".csv", "w")
    fw.write('query_prefix,topic_id,title,criteria,doc_id\n')
    for topicData in batchData[queryPrefix]:
        fw.write('{},{},"{}","{}",{}\n'.format(queryPrefix, topicData["topicId"], topicData["title"],
                                               topicData["criteria"], topicData["doc_id"]))


    fw.close()

print("Finish: generating revision batch data")