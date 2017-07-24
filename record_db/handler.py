import json
import logging
import os

import boto3
dynamodb = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def endpoint(event, context):
    logger.info("Event received: {}".format(json.dumps(event)))
    if 'email' not in event:
        logger.error("Validation Failed")
        raise Exception("Couldn't create the record: email must be present.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {k: event[k] for k in ['email', 'first_name', 'last_name']}

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }
