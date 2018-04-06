import csv
import glob

folderInput = "../Results/2018-04-05/"
blockedWorker = "A1EF7PCXWNTUXR"
outputFile = "../AMT_rejectedLists/" + blockedWorker + ".csv"


fw = open(outputFile, 'w', newline='')
csvWriter = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

countRejected = 0

for filename in glob.glob(folderInput + "*"):
    with open(filename, newline='') as inputFile:
        csvReader = csv.reader(inputFile, delimiter=',', quotechar='"')


        header = next(csvReader) #get the header row


        for row in csvReader:
            workerId = row[15]
            status = row[16]

            if workerId == blockedWorker and status=="Rejected":
                
                if countRejected == 0:
                    csvWriter.writerow(header)

                row.append('')
                row.append('x')
                countRejected += 1
                #print(workerId)
                # write only the rejected row
                csvWriter.writerow(row)
    print("Finished: {}".format(filename))
print("Count blocked: {}".format(countRejected))
fw.close()



