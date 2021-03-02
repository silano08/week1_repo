from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbsparta

# HTML을 주는 부분


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/state', methods=['GET'])
def listing():
    carriers = list(db.carriers.find({}, {'_id': False}))

    return jsonify({'all_carriers': carriers})

# API 역할을 하는 부분


@app.route('/registration', methods=['POST'])
def saving():
    carrier_receive = request.form['carrier_give']
    number_receive = request.form['number_give']

    url = 'https://apis.tracker.delivery/carriers/' + \
        carrier_receive+'/tracks/'+number_receive
    response = requests.get(url)

    carrier = response.json()['carrier']['name']
    number = number_receive
    status = response.json()['progresses'][0]['status']['text']
    desc = response.json()['progresses'][0]['description']
    loca = response.json()['progresses'][0]['location']['name']

    doc = {
        'carrier': carrier,
        'number': number,
        'status': status,
        'desc': desc,
        'loca': loca
    }

    db.carriers.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
