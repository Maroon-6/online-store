import json

secure_paths = ["/orders"]


def check_security(request, google, blueprint):
    path = request.path
    result_ok = False

    if path in secure_paths:
        google_data = None

        order_info_endpoint = '/oauth2/v2/orders'

        if google.authorized:
            google_data = google.get(order_info_endpoint).json()

            print(json.dumps(google_data, indent=2))

            s = blueprint.session
            t = s.token

            print("Token = \n", json.dumps(t, indent=2))

            result_ok = True
        else:
            result_ok = True
        return result_ok
