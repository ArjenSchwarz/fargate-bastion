from __future__ import print_function

import json
import urllib
import boto3
import datetime
import os

bastion_cluster = os.environ['BASTION_CLUSTER']
subnet_string = os.environ['BASTION_SUBNETS']
subnet_array = subnet_string.split(',')
vpc = os.environ['BASTION_VPC']

def lambda_handler(event, context):
    user = 'arjen'
    print(context)
    ip = event['requestContext']['identity']['sourceIp'] + "/32"
    ec2 = boto3.client('ec2')

    sg_response = ec2.create_security_group(
        Description='Bastion access for ' + user,
        GroupName='bastion-' + user,
        VpcId=vpc
    )

    sg = sg_response['GroupId']

    ec2.authorize_security_group_ingress(
        CidrIp=ip,
        FromPort=22,
        GroupId=sg,
        IpProtocol='tcp',
        ToPort=22
    )

    client = boto3.client('ecs')
    response = client.create_service(
        cluster=bastion_cluster,
        serviceName='bastion-' + user,
        taskDefinition='bastion-' + user,
        desiredCount=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnet_array,
                'securityGroups': [sg],
                'assignPublicIp': 'ENABLED'
            }
        }
    )

    print(event)
    print(response)
    return "{'success': true}"
