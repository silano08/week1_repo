from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/regis')
def regis():
    return render_template('regis.html')


@app.route('/regis', methods=['POST'])
def saving():
    carrier_receive = request.form['carrier_give']
    number_receive = request.form['number_give']

    carrierCode = db.carriersCode.find_one(
        {'name': carrier_receive}, {'_id': False})
    ca = carrierCode['nameCode']

    r = requests.get('https://apis.tracker.delivery/carriers/' +
                     ca+'/tracks/'+number_receive)
    result = r.json()
    print(result)

    date = result['progresses'][-1]['time'][:10]
    time = result['progresses'][-1]['time'][11:16]
    location = result['progresses'][-1]['location']['name']
    status = result['progresses'][-1]['status']['text']
    desc = result['progresses'][-1]['description']

    doc = {
        'carrier': carrier_receive,
        'number': number_receive,
        'date': date,
        'time': time,
        'location': location,
        'status': status,
        'desc': desc
    }
    db.carrierState.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
