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

questionFile = "../AMT_QualificationData/question_form.xml"
answerKeyFile = "../AMT_QualificationData/answer_key.xml"

region_name = 'us-east-1'


# load the question form
with open(questionFile, 'r') as fr:
    questionForm = fr.read()

# load the answer key
with open(answerKeyFile, 'r') as fr:
    answerKey = fr.read()

#session = boto3.Session(profile_name="default") # jimmy's AMT Sandbox
session = boto3.Session(profile_name="guido-account") # Guido's AMT

client = session.client(
    'mturk',
    endpoint_url=mturk_environment["endpoint"],
    region_name=region_name,
)


response = client.create_qualification_type(
    Name="Consumer health web assessor",
    Description="Gain 60% accuracy when assessing web pages relevance to a health topic",
    Keywords="consumer health, web pages, relevance assesment",
    RetryDelayInSeconds=60,
    QualificationTypeStatus="Active",
    Test=questionForm,
    AnswerKey=answerKey,
    TestDurationInSeconds=5*60*5,
    AutoGranted=False
)

print(response)