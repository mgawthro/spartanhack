from flask import Flask, render_template, request, jsonify, make_response, url_for
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import warnings
import json
import statistics

app = Flask(__name__)

cred = credentials.Certificate("privKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://knockknock-b4d72.firebaseio.com/'
})

database = db.reference()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/potential')
def potential():
    return render_template('potential.html')

@app.route('/current')
def current():
    return render_template('current.html')

@app.route('/handle_form_submission', methods=['POST'])
def handle_form_submission():
    # Get the selected answer from the form data
    answer_value = request.form.get('resign')

    # Perform any necessary server-side processing
    form_data_dict = request.form.to_dict()
    # Redirect based on the answer
    form_data_dict = {key: value for key, value in list(form_data_dict.items())[:-1]}

    # Redirect based on the answer
    if answer_value == 'YES':
        # mean = readjson()
        f = open('output.json')
        # returns JSON object as
        # a dictionary
        data = json.load(f)


        prices = [item["unformattedPrice"] for item in data["cat1"]["searchResults"]["listResults"]]
        print(prices)
        # Calculate the mean
        mean_price = sum(prices) / len(prices)
        my_values = [mean_price, list(form_data_dict.values())[-1]]
        return render_template('statistics.html', my_values = my_values)  # Redirect to the "statistics" route

    elif answer_value in ['NO', 'UNDECIDED']:
        return render_template('potential.html')  # Redirect to the "main" route

@app.route('/potential/getdata')
def process_button():
    # Call your Python function here
    result = fetch_json()

    listings = []
    for data in result["cat1"]["searchResults"]["mapResults"]:
        if(data["statusType"] == "FOR_RENT"):
            currList = [data["address"], data["price"]]
            if "beds" in data:
                currList.append(data["beds"])
            else:
                currList.append(data["minBeds"])
            if "baths" in data:
                currList.append(data["baths"])
            else:
                currList.append(data["minBaths"])
            if "area" in data:
                currList.append(data["area"])
            else:
                currList.append(data["minArea"])
            listings.append(currList)

    # You can do something with the result, e.g., pass it to the template
    return listings

@app.route('/app.py/potential/checkHouse/<path:input>', methods = ["POST"])
def checkDaHouse():
    try:
        data = request.form.get('input')
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("privKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://knockknock-b4d72-default-rtdb.firebaseio.com/'
        })

        # Get a reference to the root of your database
        root_ref = db.reference()

        # Query users with userName equal to "Nick123"
        query_result = root_ref.child("users").order_by_child("userName").equal_to(data).get()
        # Process the data (replace this with your actual processing logic)

        return jsonify(dict(query_result))

    except Exception as e:
        return jsonify({'error': str(e)})

def fetch_json():
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": "68c14439-3bba-4a21-9103-374f48b8d00f",
        "url":"https://www.zillow.com/ann-arbor-mi/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A42.389183%2C%22south%22%3A42.183445%2C%22east%22%3A-83.605304%2C%22west%22%3A-83.954037%7D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A8097%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
    }

    listing_response = requests.request("GET", url, params=querystring)
    print(listing_response.json()["data"])
    return listing_response.json()["data"]

def readjson():
    f = open('output.json')
    datum = json.load(f)
    prices = [item["unformattedPrice"] for item in data["cat1"]["searchResults"]["listResults"]]
    # Calculate the mean
    mean_price = sum(prices) / len(prices)
    print(mean_price)
    return mean_price, statistics.median(prices)
    
def getstats():
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": "a83eaaf4-9c4f-40bc-8160-6eb101a6c58d",
        "url":"https://www.zillow.com/ann-arbor-mi/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A42.389183%2C%22south%22%3A42.183445%2C%22east%22%3A-83.605304%2C%22west%22%3A-83.954037%7D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A8097%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
    }

    listing_response = requests.request("GET", url, params=querystring)
    data = listing_response.json()["data"]
    prices = [item["unformattedPrice"] for item in data["cat1"]["searchResults"]["listResults"]]
    # Calculate the mean
    mean_price = sum(prices) / len(prices)
    print(mean_price)
    return mean_price, statistics.median(prices)

@app.route('/api/store_data', methods=['POST'])
def store_data():
    data = request.json
    # Process and store data in the database (you can use SQLAlchemy or any other preferred database library)
    # Example: data_processing_function(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)