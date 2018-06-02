import json
import boto3
import os

delete_bastion_function = os.environ['DELETE_FUNCTION']

def lambda_handler(event, context):
    user = event['queryStringParameters']['user']
    client = boto3.client('lambda')

    client.invoke(
        FunctionName=delete_bastion_function,
        InvocationType='Event',
        Payload=bytes(json.dumps({"user": user})),
    )

    response = {}
    response['statusCode'] = 200
    return response
