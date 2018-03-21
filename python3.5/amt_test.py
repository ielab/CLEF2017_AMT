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

client = boto3.client(
    'mturk',
    endpoint_url=mturk_environment["endpoint"],
    region_name=region_name,
)


# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])