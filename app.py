from flask import Flask, Response, request, redirect, url_for
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
import json
import logging
from datetime import datetime
from middleware import notification
from middleware import security
import os

import utils.rest_utils as rest_utils

from application_services.OrdersResource.order_resource import OrderResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

null = None

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
app.secret_key = "some secret"

blueprint = make_google_blueprint(
    client_id='1027342541063-p5o91gkgoot1q6466c3tesm3gtlpce0j.apps.googleusercontent.com',
    client_secret='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',
    reprompt_consent=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")

g_bp = app.blueprints.get("google")


@app.before_request
def before_request_func():
    result_ok = security.check_security(request, google, g_bp)
    if not result_ok:
        return redirect(url_for("google.login"))


@app.after_request
def after_request_func(response):
    if response.status_code == 201:
        notification.require_sns(request)
    return response


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


@app.route('/login')
def login():
    google_data = None
    user_info_endpoint = 'oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        print(google_data)
        return "You are {email} on Google".format(email=google_data["email"])
    else:
        return redirect(url_for("google.login"))


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
            msg = "Successfully placed the order!"
            rsp = Response(json.dumps(msg, default=str), status=201, content_type="application/json")
        else:
            msg = "Failed to place the order!"
            rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/orders/<order_id>', methods=["GET"])
def specific_order(order_id):
    res = OrderResource.get_by_order_id(order_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
