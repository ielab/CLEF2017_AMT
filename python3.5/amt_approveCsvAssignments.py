import csv
import hashlib
import base64
import editdistance

salt = "ielab"
maxEditDistance = 10

folderInput = "../AMT_ResultsToBeReviewed/"
folderOutput = "../AMT_ResultsReviewed/"

fileName = "Batch_3171448_batch_results.csv"


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

        targetCompletionCode = base64.b64encode(hashlib.sha1((docId + salt).encode('utf-8')).digest()). \
            decode('utf-8')


        if len(givenCompletionCode) < 1:
            isValid = False
        else:
            isValid = editdistance.eval(givenCompletionCode, targetCompletionCode) <= maxEditDistance

        # if valid then update the Approve column with 'x'
        if isValid:
            row.append('x')
            countValid += 1

        # write the row
        csvWriter.writerow(row)

print("Count Valid: {}".format(countValid))
fw.close()



