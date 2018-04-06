# approved results from blocked worker who have refund the payment

import csv

blockedWorker = "A1EF7PCXWNTUXR"
inputFile = "../AMT_rejectedLists/" + blockedWorker + ".csv"
outputFile = "../AMT_approvedRejectedLists/" + blockedWorker + "_20180405.csv"


fw = open(outputFile, 'w', newline='')
csvWriter = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

header = ["HITId", "RequesterAnnotation", "AssignmentId", "WorkerId", "Approve"]
csvWriter.writerow(header)

countValid = 0
with open(inputFile, newline='') as inputFile:
    csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')
    next(csvReader)  #ignore the header

    for row in csvReader:
        hitId = row[0]
        requesterAnnotation = row[8]
        assignmentId = row[14]
        workerId = row[15]


        approvalRow = [hitId, requesterAnnotation, assignmentId, workerId, "x"]
        # write the row
        csvWriter.writerow(approvalRow)

fw.close()



