from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash


URI = dotenv_values('.env')['DATABASE_URI']

app = Flask(__name__)
app.secret_key = dotenv_values('.env')['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT title,time,id FROM posts"))
    posts = result.fetchall()
    return render_template("index.html", posts=posts)

@app.route("/login")
def loginpage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginaction():
    username = request.form["username"]
    password = request.form["password"]

    if verify_user(username, password):
        session["username"] = username
        return redirect("/")
    else:
        pass #ERRORMESSAGE

@app.route("/logout")
def logout_action():
    del session["username"]
    return redirect("/")

@app.route("/signup")
def sign_up():
    return render_template("create_user.html")

@app.route("/signup", methods=["POST"])
def sing_up_action():
    username = request.form["username"]
    password = request.form["password"]

    if password != request.form["password_again"]:
        return redirect("/signup") #ERRORMESSAGE
    
    passwordhash = generate_password_hash(password)
    sql = text("INSERT INTO users (username,passwordhash) VALUES (:username,:passwordhash)")
    db.session.execute(sql, {"username":username, "passwordhash":passwordhash})
    db.session.commit()

    session["username"] = username
    return redirect("/")

@app.route("/keskustelu/<int:id>")
def discussion(id):
    sql = text("SELECT * FROM posts WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    post = result.fetchone()
    username = get_user(post.user_id)
    return render_template("discussion.html", post=post, username=username)

@app.route("/uusi")
def new_post():
    return render_template("post_form.html")

@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    message = request.form["message"]

    sql = text("INSERT INTO posts (title,message,time) VALUES (:title,:message,NOW()) RETURNING id")
    result = db.session.execute(sql, {"title":title, "message":message})
    post_id = result.fetchone()[0]
    db.session.commit()
    return redirect(f"/keskustelu/{post_id}")

###################################################################
def get_user(id):
    result = db.session.execute(text("SELECT username FROM users WHERE id=:id"), {"id":id})
    username = result.fetchone()[0]
    return username

def verify_user(username, password):
    sql = text("SELECT username,passwordhash FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    existent_user = result.fetchone()
    #print(existent_user)
    if not existent_user:
        return False
    saved_hash = existent_user.passwordhash
    if check_password_hash(saved_hash, password):
        return True
    return False
