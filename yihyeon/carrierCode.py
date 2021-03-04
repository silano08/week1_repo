from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta_team_project01

@app.route('/')
def carriersCode():
    r = requests.get('https://apis.tracker.delivery/carriers')
    results = r.json()

    for result in results:
        nameCode = result['id']
        name = result['name']

        doc = {'nameCode': nameCode, 'name': name}
        db.carriersCode.insert_one(doc)


carriersCode()
