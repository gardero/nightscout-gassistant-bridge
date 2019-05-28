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
    action = req.get('queryResult').get('action')

    print(str(req))

    url = "https://test-gardero-nightscout.herokuapp.com/api/v1/entries"

    querystring = {"count":"1"}

    headers = {
        'Accept': "application/json",
        'Acces': "",
        'cache-control': "no-cache",
        'Postman-Token': "8602c936-466f-41b0-9a45-e23099216bcb"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


    # return a fulfillment response
    return {'fulfillmentText': 'Your glucose level is %d' % json.loads(response.text)[0]["sgv"]}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return json.dumps(results())


# run the app
if __name__ == '__main__':
    app.run("0.0.0.0", int(os.environ.get('PORT',5000)))

