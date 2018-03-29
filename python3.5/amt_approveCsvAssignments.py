import csv
import hashlib
import base64
import editdistance

salt = "ielab"
maxEditDistance = 10

whiteList = ["A21I4DTJGWJYQJ", "A23CV5SKZAJHQJ", "A33MF851P56BFH", "A39N0WW02VT0MB", "A1T79J0XQXDDGC",
             "A1XC5OV00MECKQ", "A2IG18D6M0GNUZ", "A1WGEJVGY3DI13"]



folderInput = "../AMT_ResultsToBeReviewed/ToAccept_2018-03-29/"
folderOutput = "../AMT_ResultsReviewed/ToAccept_2018-03-29/"

fileName = "Batch_3171314_batch_results.csv"


fw = open(folderOutput + fileName, 'w', newline='')
csvWriter = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

countValid = 0
with open(folderInput + fileName, newline='') as inputFile:
    csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')


    header = next(csvReader) #get the header row
    csvWriter.writerow(header)

    for row in csvReader:
        docId = row[32]  # get the answer.doc_id
        givenCompletionCode = row[38]
        workerId = row[15]

        targetCompletionCode = base64.b64encode(hashlib.sha1((docId + salt).encode('utf-8')).digest()). \
            decode('utf-8')


        if len(givenCompletionCode) < 1:
            isValid = False
        else:
            isValid = editdistance.eval(givenCompletionCode, targetCompletionCode) <= maxEditDistance

        # if valid then update the Approve column with 'x'
        if isValid and workerId in whiteList:
            row.append('x')
            countValid += 1

            # write the row
            csvWriter.writerow(row)

print("Count Valid: {}".format(countValid))
fw.close()



