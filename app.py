from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginpage():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    return render_template("userpage.html", username=request.form["username"])