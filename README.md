# ECIR2017_AMT
Describes Amazon Mechanical Turk settings for ECIR2017

## Create Initial HIT Project
Use sandbox to test our settings before launching it for real (i.e., cost money) .

1. login to: https://requestersandbox.mturk.com/

2. Click on the "Create" menu and then click "New Project" link.

3. Select a project template from the list.
For ECIR 2017, we use the "Sentiment of a tweet" as the starting template.
Then press the "Create Project" button.

<img src="./images/create_new_project.png" alt="Drawing" style="width: 50px;"/>

4. In tab "1. Enter Properties", supply all information requested.

5. In tab "2. Design Layout", paste content of the amt_page.html into the source

6. Preview and if everything looks good, then press the Finish button


## Create Qualification Test
To create a qualification test, we need to use the AMT API.
Here, we are going to use Python 3.6 with the AMT API.

1. From the requester sandbox mturk site (https://requestersandbox.mturk.com/), click on the Developer menu

2. Press Link your AWS Account (need to create one) and follow the instructions.

3. After accounts successfully linked, press link "Get your AWS Access Key"

<img src="./images/successfully_linked_to_aws.png" alt="Drawing" style="width: 50px;"/>

4. In the aws site, choose continue to IAM users then click "Add user"

5. Type in username and tick "Programmatic access" access type. Click Next: Permissions.

6. In the next screen, we need to create a group with access to all AMT APIs. Click "Create group"

7. In the Create group box, define the group name and tick the "AmazonMechanicalTurkFullAccess" policy

<img src="./images/create_aws_user_group.png" alt="Drawing" style="width: 50px;"/>

8. Click Next: Review, and if all good, then click Create user to finalise the user.

9. The new user will now be in the user list along with information on access key id and secret access key.
We will need both of these keys to use the AMT APIs.



## Configure the AWS CLI

1. Install AWS CLI (follow instructions from: https://aws.amazon.com/cli/)

2. Configure aws using Access Key and Secret access key that we just created.
```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-2
Default output format [None]: json
```


## Setup Boto3 to enable AMT APIs access using python.

 1. Follow instructions from: https://katherinemwood.github.io/post/mturk_dev_intro/


## Crete qualification type
 1. Create question form as in the question_form.xml

 2. Create answer key as in the answer_key.xml

 3. The question form and the answer key is part of the qualification type configuration:
 ```
 client.create_qualification_type(
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
 ```

 Run the amt_createQualificationType.py to execute the above script.

