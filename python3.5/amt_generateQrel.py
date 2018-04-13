# this script reads results from AMT in CSV files to generate QREL
import csv
import glob
from collections import defaultdict
from lxml import etree

blockedWorkers = ["A1EF7PCXWNTUXR", "A2SKH7WZUEDGGI", "AH4SMMFHDHK1L", "A1XA2WZVXTTLOI", "A3RYO4RE80IJ84",
                  "A3S104I5V53HB8", "AZ7GSYRVDR23N", "A1XZTIJD9WBHLJ", "A2XYDJS33I2341", "AZZM966F90AL1",
                  "A3B67I3A0YR2D", "A1PLY1H54IPJRB", "A1T1FK3P2N408U", "A2LO2DX6H49IKW", "A1RU9BQLDZ1DSY",
                  "AKATSYE8XLYNL"]

# filename with results from relevation for query prefix 101 to 105
relevationQrelFile = "../qrels.clef2017.101-105"
relevationQreadFile = "../qreads.clef2017.101-105"
relevationQtrustFile = "../qtrust.clef2017.101-105"

# folder with results from AMT for query prefix 106 to 150
folderInput = "../Results/"


queryFile = '/volumes/Data/Phd/Data/Clef2017_eval/queries2016.xml'

outQrel = "../clef2017_qrels.txt"
outQread = "../clef2017_qreads.txt"
outQtrust = "../clef2017_qtrust.txt"

qrelData = defaultdict(list)
qreadData = defaultdict(list)
qtrustData = defaultdict(list)

print("Loading qrel from relevation")
with open(relevationQrelFile, "r") as inputFile:
    for line in inputFile:
        queryPrefix, temp1, docId, relScore = line.strip().split(" ")
        qrelData[queryPrefix].append({"docId": docId, "relScore": relScore})


print("Loading qread from relevation")
with open(relevationQreadFile, "r") as inputFile:
    for line in inputFile:
        queryPrefix, temp1, docId, readScore = line.strip().split(" ")
        qreadData[queryPrefix].append({"docId": docId, "readScore": readScore})


print("Loading qtrust from relevation")
with open(relevationQtrustFile, "r") as inputFile:
    for line in inputFile:
        queryPrefix, temp1, docId, trustScore = line.strip().split(" ")
        qtrustData[queryPrefix].append({"docId": docId, "trustScore": trustScore})


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
                    readScore = row[header.index("Answer.readability")]
                    trustScore = row[header.index("Answer.reliability")]

                    qrelData[queryPrefix].append({"docId": docId, "relScore": relScore})
                    qreadData[queryPrefix].append({"docId": docId, "readScore": readScore})
                    qtrustData[queryPrefix].append({"docId": docId, "trustScore": trustScore})


tree = etree.parse(queryFile)
topics = tree.getroot()

fwRel = open(outQrel, "w")
fwRead = open(outQread, "w")
fwTrust = open(outQtrust, "w")

print("generating qrels")
for topic in topics.iter("query"):
    for detail in topic:
        if detail.tag == "id":
            queryNumber = detail.text

    print("{}:{} ".format(queryNumber, len(qrelData[queryNumber[:3]])))
    for qData in qrelData[queryNumber[:3]]:
        fwRel.write("{} 0 {} {}\n".format(queryNumber, qData["docId"], qData["relScore"]))

    for qData in qreadData[queryNumber[:3]]:
        fwRead.write("{} 0 {} {}\n".format(queryNumber, qData["docId"], qData["readScore"]))

    for qData in qtrustData[queryNumber[:3]]:
        fwTrust.write("{} 0 {} {}\n".format(queryNumber, qData["docId"], qData["trustScore"]))

fwRel.close()
fwRead.close()
fwTrust.close()
print("finish all")