from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for

from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
db = client.dbsparta_team_project01

# html파일 불러오기
@app.route('/')
def home():
    return render_template('index.html')

# 회원가입 페이지 불러오기
@app.route('/sign_up')
def sign_up():
    return render_template('signup.html')

# 회원가입
@app.route('/sign_up/register', methods=['POST'])
def register():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username": username_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # db에 데이터 넣고 조회 한 결과
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    # 회원인 경우
    if result is not None:
        # user id와 로그인 유효기간을 payload에 담고
        payload = {
            'id': username_receive,
            # 24시간 동안 로그인 유지할 수 있게 하는 유효기간 설정
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        # payload를 시크릿키로 감싸서 암호화 한 다음에 token 발행.
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # 결과적으로 회원에게 강력히 암호화된 토큰을 만들어 줌.
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공!'})

    # 회원이 아닌 경우(아이디나 비밀번호를 잘못 입력 했을 때)
    else:
        return jsonify({'result': 'fail', 'msg': '아이디나 비밀번호가 맞지 않습니다. 다시 확인해주세요.'})


# 회원가입
# @app.route('/sign_up', methods=['POST'])
# def sign_up():
#     return jsonify({'result': 'success', 'msg': '회원가입 접속 성공!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)