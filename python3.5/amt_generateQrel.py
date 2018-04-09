# this script reads results from AMT in CSV files to generate QREL
import csv
import glob
from collections import defaultdict
from lxml import etree

blockedWorkers = ["A1EF7PCXWNTUXR", "A2SKH7WZUEDGGI", "AH4SMMFHDHK1L", "A1XA2WZVXTTLOI", "A3RYO4RE80IJ84",
                  "A3S104I5V53HB8", "AZ7GSYRVDR23N", "A1XZTIJD9WBHLJ", "A2XYDJS33I2341", "AZZM966F90AL1",
                  "A3B67I3A0YR2D", "A1PLY1H54IPJRB", "A1T1FK3P2N408U", "A2LO2DX6H49IKW", "A1RU9BQLDZ1DSY",
                  "AKATSYE8XLYNL"]

folderInput = "../Results/"
queryFile = '/volumes/Data/Phd/Data/Clef2017_eval/queries2016.xml'

outQrel = "../clef2017_qrel.txt"

qrelData = defaultdict(list)
print("Loading results")
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

                    qrelData[queryPrefix].append({"docId": docId, "relScore": relScore})


tree = etree.parse(queryFile)
topics = tree.getroot()

fw = open(outQrel, "w")
print("generating qrels")
for topic in topics.iter("query"):
    for detail in topic:
        if detail.tag == "id":
            queryNumber = detail.text

    print("{}:{} ".format(queryNumber, len(qrelData[queryNumber[:3]])))
    for qData in qrelData[queryNumber[:3]]:
        fw.write("{} 0 {} {}\n".format(queryNumber, qData["docId"], qData["relScore"]))

fw.close()

print("finish all")