# approve assigment with correct completion type

import hashlib
import base64
import boto3
import editdistance
import xml.etree.ElementTree as ET


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

salt = "ielab"
maxEditDistance = 5

# get list of HITs
hitCount = {}
submittedCount = {}
validCount = {}
invalidCount = {}

hasMoreHit = True
nextToken = ""
while hasMoreHit:
    if nextToken == "":
        resHits = client.list_reviewable_hits(MaxResults=100)
    else:
        resHits = client.list_reviewable_hits(MaxResults=100, NextToken=nextToken)
    #print(resHits)

    for hit in resHits["HITs"]:
        #print("HItId:{}".format(hit["HITId"]))

        batchId = hit["RequesterAnnotation"]
        batchId = batchId.split(";")[0]
        batchId = batchId.split(":")[1]

        if batchId not in hitCount:
            hitCount[batchId] = 1
            submittedCount[batchId] = 0
            validCount[batchId] = 0
            invalidCount[batchId] = 0
        else:
            hitCount[batchId] += 1



        # obtain validation code
        # get list of assignment for current Hit, since we only have 1 assignment per hit, we don't handle paging
        givenCompletionCode = ""
        targetCompletionCode = ""
        resAssignments = client.list_assignments_for_hit(HITId=hit["HITId"], AssignmentStatuses=["Submitted"])
        if len(resAssignments["Assignments"]) > 0:
            for assignment in resAssignments["Assignments"]:
                assignmentId = assignment["AssignmentId"]
                submittedCount[batchId]+1
                #print(assignment)
                answersNode = ET.fromstring(assignment['Answer'])

                for answerNode in answersNode:
                    answerValue = ""
                    for valueNode in answerNode:
                        variableName = valueNode.tag.split("}")[1]
                        if variableName == "QuestionIdentifier":
                            question = valueNode.text
                        elif variableName == "FreeText":
                            answerValue = valueNode.text
                    #print("{}: {}".format(question, answerValue))

                    if question == "validationCode":
                        givenCompletionCode = answerValue
                        #print("Validation Code: {}".format(givenCompletionCode))
                    elif question == "doc_id":
                        docId = answerValue
                        #print("docId: {}".format(docId))

                        targetCompletionCode = base64.b64encode(hashlib.sha1((docId + salt).encode('utf-8')).digest()).\
                            decode('utf-8')

                if len(givenCompletionCode)<1:
                    isValid = False
                else:
                    isValid = editdistance.eval(givenCompletionCode,targetCompletionCode) <= maxEditDistance

                print("BatchId:{} HitId: {} AssignmentId:{} given:{} target:{} isValid:{}".
                      format(batchId, hit["HITId"], assignmentId, givenCompletionCode, targetCompletionCode, isValid))

                if isValid:
                    validCount[batchId] += 1
                    resApprove = client.approve_assignment(AssignmentId=assignmentId)
                    print(resApprove)

                else:
                    invalidCount[batchId] += 1




    if "NextToken" in resHits:
        nextToken= resHits["NextToken"]
    else:
        hasMoreHit = False


for batchId in hitCount:
    print("{}: Total:{} Submitted:{} valid:{} invalid:{}".format(batchId, hitCount[batchId], submittedCount[batchId],
                                                                 validCount[batchId], invalidCount[batchId]))



