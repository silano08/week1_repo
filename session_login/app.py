from flask import url_for,session,Flask,render_template,request,redirect

app = Flask(__name__)
app.secret_key = "geung_geung"

ID = "hello"
PW = "world"

@app.route("/")
def home():
    if "userID" in session:
        return render_template("home.html",username = session.get("userID"),login=True)
    else:
        return render_template("home.html",login=False)

@app.route("/login", methods=["get"])
def login():
    global ID,PW
    _id_ = request.args.get("loginId")
    _password_ = request.args.get("loginPw")

    # 밑의 조건문을 통해 home으로 돌아가는데 세션아이디가 있고없고의차이
    if ID == _id_ and _password_ ==PW:
        session["userID"] = _id_
        return redirect(url_for("home"))
    else: 
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect(url_for("home"))

@app.route("/signup")
def signup():
    pass

app.run(host="0.0.0.0",port=5000)