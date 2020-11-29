from price_scraper import scrape_amazon_search

from flask import Flask, request, render_template, jsonify
import requests 
import json
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from datetime import datetime
import os 

# Set .env vars
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    search_term = str(request.form['test'])

    now = datetime.now()
    dt_str = now.strftime("%H:%M:%S %B %d, %Y ")
    
    ACCESS_KEY = os.getenv("AWSAccessKeyId")
    SECRET_KEY = os.getenv("AWSSecretKey")
    BUCKET_NAME = "amazon-search-results"
    FILE_NAME = dt_str + "searched_products.json"

    products = scrape_amazon_search(search_term)

    with open('products.json', 'w') as json_file:
        json.dump(products, json_file, sort_keys=True, indent=4)

    s3 =  boto3.resource(
                        's3', 
                        aws_access_key_id = ACCESS_KEY,
                        aws_secret_access_key = SECRET_KEY,
                    )
                    

    try:
        s3.Bucket(BUCKET_NAME).upload_file("products.json", FILE_NAME)
        print("Upload Successful")
    except FileNotFoundError: 
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)