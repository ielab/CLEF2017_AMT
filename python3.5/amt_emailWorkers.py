import boto3

salt = "ielab"
maxEditDistance = 10

whiteList = ["A21I4DTJGWJYQJ", "A23CV5SKZAJHQJ", "A33MF851P56BFH", "A39N0WW02VT0MB", "A1T79J0XQXDDGC",
             "A1XC5OV00MECKQ", "A2IG18D6M0GNUZ", "A1WGEJVGY3DI13"]


stringSubject = "Invitation to work on Assess relevance of webpage to health topic (Tasks 46 to 50)"
stringMessage = "Dear AMT Workers,\n" \
                "We are pleased to invite you to work on our final 5 HITs for assessing relevance of a webpage to a health topic.\n" \
                "We are looking forward to receive high quality assessments from you.\n\n" \
                "Thank you.\n\n" \
                "Regards,\n" \
                "Jimmy"

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


resMessage = client.notify_workers(Subject=stringSubject, MessageText=stringMessage, WorkerIds=whiteList)
print(resMessage)

