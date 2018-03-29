import csv
import hashlib
import base64
import editdistance

salt = "ielab"
maxEditDistance = 10

blockedWorkers = ["A1EF7PCXWNTUXR", "A2SKH7WZUEDGGI", "AH4SMMFHDHK1L", "A1XA2WZVXTTLOI", "A3RYO4RE80IJ84",
                  "A3S104I5V53HB8", "AZ7GSYRVDR23N", "A1XZTIJD9WBHLJ", "A2XYDJS33I2341", "AZZM966F90AL1",
                  "A3B67I3A0YR2D", "A1PLY1H54IPJRB", "A1T1FK3P2N408U", "A2LO2DX6H49IKW", "A1RU9BQLDZ1DSY",
                  "AKATSYE8XLYNL"]

folderInput = "../AMT_ResultsToBeReviewed/"
folderOutput = "../AMT_ResultsRejected/"

fileName = "2018-03-29/Batch_3171314_batch_results.csv"


fw = open(folderOutput + fileName, 'w', newline='')
csvWriter = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

countRejected = 0
with open(folderInput + fileName, newline='') as inputFile:
    csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')


    header = next(csvReader) #get the header row
    csvWriter.writerow(header)

    for row in csvReader:
        workerId = row[15]


        if workerId in blockedWorkers:
            row.append('')
            row.append('x')
            countRejected += 1
            #print(workerId)
            # write only the rejected row
            csvWriter.writerow(row)

print("Count blocked: {}".format(countRejected))
fw.close()



