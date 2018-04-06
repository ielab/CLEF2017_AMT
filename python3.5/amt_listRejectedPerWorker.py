# list rejected assignments for a worker
import boto3

mode = "live"

environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
        }
}
mturk_environment = environments[mode]
region_name = 'us-east-1'

session = boto3.Session(profile_name="guido-account") # Guido's AMT

client = session.client(
    'mturk',
    endpoint_url=mturk_environment["endpoint"],
    region_name=region_name,
)

workerId = "A1EF7PCXWNTUXR"
outputFile = "../AMT_rejectedLists/" + workerId + ".csv"

fw = open(outputFile, 'w')
fw.write("workerId, batchId, AssignmentId, Status \n")

# get list of HITs
hitCount = {}
workerRejectCount = {}
totalRejectCount = {}
overalWorkerRejectCount = 0

hasMoreHit = True
nextToken = ""
while hasMoreHit:
    if nextToken == "":
        resHits = client.list_hits(MaxResults=100)
    else:
        resHits = client.list_hits(MaxResults=100, NextToken=nextToken)
    #print(resHits)

    for hit in resHits["HITs"]:
        batchId = hit["RequesterAnnotation"]
        batchId = batchId.split(";")[0]
        batchId = batchId.split(":")[1]

        if batchId not in hitCount:
            hitCount[batchId] = 1
            workerRejectCount[batchId] = 0
            totalRejectCount[batchId] = 0
        else:
            hitCount[batchId] += 1

        # get list of rejected assignment for current Hit, since we only have 1 assignment per hit, we don't handle paging
        resAssignments = client.list_assignments_for_hit(HITId=hit["HITId"], AssignmentStatuses=["Rejected"])
        if len(resAssignments["Assignments"]) > 0:
            for assignment in resAssignments["Assignments"]:
                totalRejectCount[batchId] += 1
                #check if assingment is for the targeted worker
                if assignment["WorkerId"] == workerId:
                    assignmentId = assignment["AssignmentId"]
                    fw.write("{}, {}, {}, {} \n".format(assignment["WorkerId"], batchId, assignment["AssignmentId"],
                                                        assignment["AssignmentStatus"]))
                    workerRejectCount[batchId] += 1
                    overalWorkerRejectCount += 1

    # print some progress
    print("Last batchId:{} Total Worker Reject: {}".format(batchId, overalWorkerRejectCount))

    if "NextToken" in resHits:
        nextToken= resHits["NextToken"]
    else:
        hasMoreHit = False

fw.close()

for batchId in hitCount:
    print("{}: Total:{} TotalRejects:{} WorkerRejected:{} overWorkerReject:{}".
          format(batchId, hitCount[batchId], totalRejectCount[batchId], workerRejectCount[batchId],
                 overalWorkerRejectCount))



