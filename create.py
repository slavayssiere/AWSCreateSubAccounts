import boto3
import time
from assume_role import * 

account = input("please enter new account name:")

# create the account in AWS organizations
client = boto3.client('organizations')
response = client.create_account(
    Email='aws-vwt-master+'+account.replace(" ", "")+'@veolia.com',
    AccountName=account,
    RoleName='AccountAccessRole',
    IamUserAccessToBilling='DENY'
)
print(response)

account_id = response['CreateAccountStatus']['AccountId']
print(account_id)

# wait for account creation
create_success = False
while create_success == False:
    response = client.list_create_account_status(
        States=[
            'IN_PROGRESS'
        ]
    )
    print(response)
    if len(response['CreateAccountStatuses'])==0:
        create_success = True
    time.sleep(20) # wait 20 seconds
    
        

# connect to the new account
sts = boto3.client('sts')
sts_response = sts.assume_role(
    RoleArn = "arn:aws:iam::"+account_id+":role/AccountAccessRole",
    RoleSessionName = "AccountAccessRole",
)

client = boto3.client(
    'iam',
    region_name='eu-west-1',
    aws_access_key_id = sts_response['Credentials']['AccessKeyId'],
    aws_secret_access_key = sts_response['Credentials']['SecretAccessKey'],
    aws_session_token = sts_response['Credentials']['SessionToken'])

## create role and policy
jenkins_to_create = {
    Name='JenkinsIam',
    Policy='JenkinsPolicy',
    PolicyDescription='Use to allow Jenkins and Travis to apply policy creation',
    RoleDescription='',
    PolicyName='',
    PolicyDocument=jenkins_policy_role,
    AssumeRolePolicyDocument=jenkins_iam_assume_role
}

create_role_policy(client,jenkins_to_create)

print("success !")


def create_role_policy(client,role):
    
    # path define to / by default

    response = client.create_policy(
        PolicyName=role.PolicyName,
        PolicyDocument=role.PolicyDocument,
        Description=role.PolicyDescription
    )

    response = client.create_role(
        RoleName=role.Name,
        AssumeRolePolicyDocument=role.AssumeRolePolicyDocument,
        Description=role.RoleDescription
    )