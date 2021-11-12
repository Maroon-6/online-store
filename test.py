import boto3
import json


def test_sns():
    client = boto3.client('sns', region_name="us-east-1")
    msg = "A new order has been placed!"
    client.publish(TopicArn="arn:aws:sns:us-east-1:493194649607:place_order_notification",
                   Message=json.dumps(msg))
