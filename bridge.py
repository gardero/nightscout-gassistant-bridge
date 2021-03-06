import os

from flask import Flask, request
import json
import requests

# initialize the flask app
app = Flask(__name__)


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('intent').get('displayName')

    print(str(req))
    print("Intent "+action)

    if action == "glucose-level":
        url = "%s/api/v1/entries" % os.environ.get('NIGHTSCOUT_ADDRESS')
        querystring = {"count": "1"}
        response = call_api(querystring, url)
        # return a fulfillment response
        return {'fulfillmentText': 'Your glucose level is %d' % json.loads(response.text)[0]["sgv"]}
    if action == "carbs-insulin-intake":
        # url = "%s/api/v1/entries" % os.environ.get('NIGHTSCOUT_ADDRESS')
        # querystring = {"count": "1"}
        # response = call_api(querystring, url, "POST")
        # # return a fulfillment response
        return {'fulfillmentText': 'Sorry, the functionality is not completely implemented'}
    else:
        return {'fulfillmentText': 'Sorry, I cannot provide that information'}


def call_api(querystring, url, method="GET"):
    headers = {
        'Accept': "application/json",
        'Acces': "",
        'cache-control': "no-cache",
        'Postman-Token': "8602c936-466f-41b0-9a45-e23099216bcb"
    }
    print("calling: " + url)
    response = requests.request(method, url, headers=headers, params=querystring)
    print(response.text)
    return response


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return json.dumps(results())


@app.route('/', methods=['GET'])
def default():
    # return response
    return "all good"


# run the app
if __name__ == '__main__':
    app.run("0.0.0.0", int(os.environ.get('PORT',5000)))

