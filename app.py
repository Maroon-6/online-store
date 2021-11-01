from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
import boto3
from datetime import datetime

import utils.rest_utils as rest_utils

from application_services.OrdersResource.order_resource import OrderResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


##################################################################################################################

# DFF TODO A real service would have more robust health check methods.
# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp


# TODO Remove later. Solely for explanatory purposes.
# The method take any REST request, and produces a response indicating what
# the parameters, headers, etc. are. This is simply for education purposes.
#
@app.route("/api/demo/<parameter1>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/api/demo/", methods=["GET", "POST", "PUT", "DELETE"])
def demo(parameter1=None):
    """
    Returns a JSON object containing a description of the received request.

    :param parameter1: The first path parameter.
    :return: JSON document containing information about the request.
    """

    # DFF TODO -- We should wrap with an exception pattern.
    #

    # Mostly for isolation. The rest of the method is isolated from the specifics of Flask.
    inputs = rest_utils.RESTContext(request, {"parameter1": parameter1})

    # DFF TODO -- We should replace with logging.
    r_json = inputs.to_json()
    msg = {
        "/demo received the following inputs": inputs.to_json()
    }
    print("/api/demo/<parameter> received/returned:\n", msg)

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/orders', methods=['GET', 'POST'])
def order_collection():
    if request.method == 'GET':
        res = OrderResource.get_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'POST':
        data = request.json
        res = OrderResource.place_order(data)
        if res:
            now = datetime.now()
            msg = "A new order has been placed on " + now.strftime("%m/%d/%Y, %H:%M:%S") + "!"
            send_sns_msg(msg)
        else:
            msg = "Failed to place the order!"
        rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/orders/<order_id>', methods=["GET"])
def specific_order(order_id):
    res = OrderResource.get_by_order_id(order_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


def send_sns_msg(msg):
    client = boto3.client('sns', region_name="us-east-1")
    client.publish(TopicArn="arn:aws:sns:us-east-1:493194649607:place_order_notification",
                   Message=json.dumps(msg))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
