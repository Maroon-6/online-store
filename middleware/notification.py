import boto3
import json
from datetime import datetime


PATHS = {'/orders': 'POST'}


def require_sns(request):
    path = request.path
    method = request.method
    if PATHS.get(path, None) == method:
        now = datetime.now()
        msg = "A new order has been placed on " + now.strftime("%m/%d/%Y, %H:%M:%S") + "!"
        client = boto3.client('sns', region_name="us-east-1")
        client.publish(TopicArn="arn:aws:sns:us-east-1:493194649607:place_order_notification",
                       Message=json.dumps(msg))
