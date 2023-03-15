from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import dotenv_values

URI = dotenv_values('.env')['DATABASE_URI']

app = Flask(__name__)
print(URI)
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

@app.route("/", methods=["POST"])
def loginaction():
    return render_template("userpage.html", username=request.form["username"])

@app.route("/keskustelu/<int:id>")
def discussion(id):
    sql = text("SELECT * FROM posts WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    post = result.fetchone()
    username = get_user(post.user_id)
    return render_template("discussion.html", post=post, username=username)

@app.route("/uusi")
def new_post():
    return

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
