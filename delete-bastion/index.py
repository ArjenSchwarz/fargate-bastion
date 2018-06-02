from __future__ import print_function

import urllib
import boto3
from botocore.exceptions import ClientError
import datetime
import os
import time
import re

bastion_cluster = os.environ['BASTION_CLUSTER']
vpc = os.environ['BASTION_VPC']

def successResponse():
    response = {}
    response['statusCode'] = 200
    return response

def failResponse(error):
    response = {}
    response['statusCode'] = 500
    response['body'] = error
    return response

def lambda_handler(event, context):
    user = event['user']
    ec2 = boto3.client('ec2')
    ecs = boto3.client('ecs')

    bastion_name = 'bastion-' + user
    print("Starting to delete")

    try:
        # Find the Fargate task
        running_tasks = ecs.list_tasks(
            cluster=bastion_cluster,
            family=bastion_name,
            desiredStatus='RUNNING'
        )
        for task_arn in running_tasks['taskArns']:
            print("Found a task")
            # Retrieve the ENI information
            tasklist = ecs.describe_tasks(
                cluster=bastion_cluster, tasks=[task_arn])
            attachment_id = tasklist['tasks'][0]['attachments'][0]['id']
            attachment_identifier = "attachment/" + attachment_id
            attachment_description = re.sub(
                r'task/.*', attachment_identifier, task_arn)
            # Stop the task
            ecs.stop_task(
                cluster=bastion_cluster,
                task=task_arn,
                reason='Requested by user'
            )
            # Wait until the ENI is deleted to prevent dependency conflict for removing security group
            eni_description = ec2.describe_network_interfaces(
                Filters=[
                    {
                        'Name': 'description',
                        'Values': [attachment_description]
                    }
                ]
            )
            while len(eni_description['NetworkInterfaces']) > 0:
                time.sleep(2)
                eni_description = ec2.describe_network_interfaces(
                    Filters=[
                        {
                            'Name': 'description',
                            'Values': [attachment_description]
                        }
                    ]
                )
        print("Task is deleted")
        # Now find the security group to delete
        security_group = ec2.describe_security_groups(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc]},
                {'Name': 'group-name', 'Values': [bastion_name]}
            ]
        )
        for group in security_group['SecurityGroups']:
            ec2.delete_security_group(GroupId=group['GroupId'])

        print("Groups are deleted")

    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
            print("SecurityGroup doesn't exist, skipping deletion")
        else:
            failResponse(e.response)

    return successResponse()