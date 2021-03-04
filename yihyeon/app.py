from pymongo import MongoClient
import requests
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SECRET_KEY = 'SPARTA'   # 우리 팀 걸로 설정 맞추기.

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta_team_project01


# html파일 불러오기


@app.route('/')
def home():
    return render_template('index.html')

# 회원가입 페이지 불러오기


@app.route('/sign_up')
def sign_up():
    return render_template('signup.html')

# 택배조회 페이지 불러오기


@app.route('/show_mylist')
def show_mylist():

    # 토큰 꺼내오기
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = db.users.find_one({"username": payload["id"]})['username']
        print(user_id)
        return render_template('mylist.html', user_info=user_id)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 택배조회 페이지에 아이디 던져주기
# @app.route('/show_mylist', methods=['POST'])
# def get_username():
#
#     return jsonify({'result': 'success'})

#
# @app.route('/result', methods=['GET'])
# def result():
#     # user_id = request.form['userid']
#     user_id = request.args.get('userid')
#
#     return render_template('mylist.html', user_id)


# 회원가입
@app.route('/sign_up/register', methods=['POST'])
def register():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    password_hash = hashlib.sha256(
        password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username": username_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    print(db.users.find_one({"username": username_receive}))
    print(bool(db.users.find_one({"username": username_receive})))
    return jsonify({'result': 'success', 'exists': exists})


# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # db에 데이터 넣고 조회 한 결과
    result = db.users.find_one(
        {'username': username_receive, 'password': pw_hash})

    # 회원인 경우
    if result is not None:
        # user id와 로그인 유효기간을 payload에 담고
        payload = {
            'id': username_receive,
            # 24시간 동안 로그인 유지할 수 있게 하는 유효기간 설정
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        # 클라이언트에게 토큰 전달
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공!'})

    # 회원이 아닌 경우(아이디나 비밀번호를 잘못 입력 했을 때)
    else:
        return jsonify({'result': 'fail', 'msg': '아이디나 비밀번호가 맞지 않습니다. 다시 확인해주세요.'})


# 포스팅
@app.route('/regis', methods=['POST'])
def regis():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})["username"]
        carrier_receive = request.form["carrier_give"]
        number_receive = request.form["number_give"]

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
            "username": user_info,
            'carrier': carrier_receive,
            'number': number_receive,
            'date': date,
            'time': time,
            'location': location,
            'status': status,
            'desc': desc
        }

        # doc = {
        #     "username": user_info["username"],
        #     "profile_name": user_info["profile_name"],
        #     "profile_pic_real": user_info["profile_pic_real"],
        #     "carrier": carrier_receive,
        #     "number": number_receive
        # }

        db.useruser.insert_one(doc)
        return jsonify({"result": "success", 'msg': '등록 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


# 배송중인 택배 총 건수
# @app.route('/get_amount', methods=['GET'])
# def get_amount():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         users = list(db.useruser.find({}).sort("date", -1).sort("time", -1))
#         print(users)
#         for user in users:
#             user["_id"] = str(user["_id"])
#         return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "users": users})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("index"))
#     return jsonify({'msg':'GET 연결되었습니다!'})


# 포스트 요청하여 브라우저에 보여주기
@app.route("/get_regis", methods=['GET'])
def get_regis():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        users = list(db.useruser.find({"username": payload["id"]}).sort("date", -1).sort("time", -1))
        print(users)
        for user in users:
            user["_id"] = str(user["_id"])
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "users": users})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)