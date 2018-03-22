import boto3

mode = "sandbox"

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


session = boto3.Session(profile_name="guido-account")
client = session.client(
    'mturk',
    endpoint_url=mturk_environment["endpoint"],
    region_name=region_name,
)


# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])


# Check qualification type
print(client.get_qualification_type(
    QualificationTypeId="3GDU63T2RFMVPA5LW62U4HQZG8SEA1"))

