from argon2 import PasswordHasher
import boto3
import os
import json
import time


## Create IAM role policy
def CreateInstanceProfileRole():
    client = boto3.client('iam')
    assume_role_policy_document = json.dumps({ "Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}
        ]
    })

    ## Create IAM role
    create_role_response = client.create_role(RoleName = "my-instance-role", AssumeRolePolicyDocument = assume_role_policy_document)
    print (create_role_response)

    ## Attach policies to above role
    roleSSMpolicyAttachResponse = client.attach_role_policy( RoleName='my-instance-role', PolicyArn='arn:aws:iam::aws:policy/AmazonSSMFullAccess')
    print (roleSSMpolicyAttachResponse)

    ## Attach policies to above role
    roleS3policyAttachResponse = client.attach_role_policy( RoleName='my-instance-role', PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
    print (roleS3policyAttachResponse)

    ## Create instance profile
    instance_profile = client.create_instance_profile ( InstanceProfileName ='Test-instance-profile')
    print (instance_profile)
    ## Add roles
    response = client.add_role_to_instance_profile ( InstanceProfileName = 'Test-instance-profile', RoleName = 'my-instance-role')
    print (response)

## Create EC2 key pair
def create_key_pair():
    print("I am inside key pair generation..")
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName="ec2-key-pair")

    private_key = key_pair["KeyMaterial"]

    ## write private key to file with 400 permissions
    with os.fdopen(os.open("F:/RekhuAll/AWS/PythonAllAWS/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle: handle.write(private_key)

## Create VPC
def create_aws_vpc():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    vpc = ec2_client.create_vpc( CidrBlock='172.16.0.0/16' )
    print ("Successfully created vpc details are -  {}".format(vpc))
    subnet = ec2_client.create_subnet(CidrBlock = '172.16.2.0/24', VpcId= vpc['Vpc']['VpcId'])
    print("Successfully created subnet details are -  {}".format(subnet))
    return subnet['Subnet']['SubnetId']


## EC2 instance boto3
def create_instance(subnet):
    print("Create AWS instances..")
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    instances = ec2_client.run_instances(ImageId="ami-052efd3df9dad4825", MinCount=1, MaxCount=1, InstanceType="t2.micro",KeyName="ec2-key-pair", IamInstanceProfile={'Name': "Ahmedtest"},SecurityGroupIds=['sg-03241488f1f004306'] )
    return instances["Instances"][0]["InstanceId"]

## How to get the public IP for a running EC2 instance
def get_public_ip(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))

## How to list all running EC2 instances
def get_running_instancesids():
    Instance_list=[]
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            Instance_list.append(instance_id)
    return(Instance_list)
def get_running_instancesips():
    Instance_list=[]
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            Instance_list.append(public_ip)
    return(Instance_list)

## Run command against your linux VM
def runRemoteShellCommands (InstanceId,i):
    ssm_client = boto3.client('ssm', region_name="us-east-1") 
    response = ssm_client.send_command( InstanceIds=[InstanceId], DocumentName="AWS-RunShellScript", Parameters={'commands':[i]},)
    command_id = response['Command']['CommandId']
    output = ssm_client.get_command_invocation( CommandId=command_id, InstanceId=InstanceId)
    while output['Status'] == "InProgress":   
        output = ssm_client.get_command_invocation( CommandId=command_id, InstanceId=InstanceId)
    print(output['StandardOutputContent'])
    print(output['StatusDetails'])
    print(output['StandardErrorContent'])

#CreateInstanceProfileRole()

#create_key_pair()


#get_public_ip("i-0016f12e547e92072")




    
    