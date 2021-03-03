from flask import url_for,session,Flask,render_template,request,redirect
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
app.secret_key = "geung_geung"

client = MongoClient('localhost', 27017)
db = client.bojaboja_service


@app.route('/')
def login():
    if "userID" in session:
        return render_template("login.html", username=session.get("userID"),login=True)
    else:
        return render_template("login.html", login=False)

@app.route('/home', methods=["GET"])
def home():
    _id_ = request.args.get("loginId")
    _password_ = request.args.get("loginPw")

    result = db.users.bojaboja_service.find_one({'userid': _id_, 'userpwd': _password_})
    # 밑의 조건문을 통해 login으로 돌아가는데 세션아이디가 있고없고의차이
    # if ID == _id_ and _password_ ==PW:
    if result is not None:
        session["userID"] = _id_
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/signin', methods=["get"])
def signin():
    return render_template('signin.html')


@app.route("/signin_done", methods=["get"])
def signin_done():
    username = request.args.get("name")
    userid = request.args.get("id")
    userpwd = request.args.get("Pw")

    doc = {
        # 이후 다른 post 정보도 삽입가능, 그런데 그건 다른함수에 넣을예정
        'username':username,
        'userid': userid,
        'userpwd': userpwd
    }

    # db.users.bojaboja_service.insert_one(doc)
    # return redirect(url_for("signin"))

    result = db.users.bojaboja_service.find_one({'userid': userid, 'userpwd': userpwd})

    # 밑의 조건문을 통해 login으로 돌아가는데 세션아이디가 있고없고의차이
    # if ID == _id_ and _password_ ==PW:
    if result is not None:
        return redirect(url_for("signin"))
    else:
        db.users.bojaboja_service.insert_one(doc)
        return redirect(url_for("login"))

@app.route("/login_done")
def login_done():
    pass

@app.route('/logout')
def logout():
    session.pop("userID")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)