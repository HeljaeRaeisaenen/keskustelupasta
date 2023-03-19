from app import app
import users
import discussions
import comments
from flask import render_template, request, redirect, session

@app.route("/")
def index():
    posts = discussions.get_all_posts()
    return render_template("index.html", posts=posts)

@app.route("/login")
def loginpage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginaction():
    username = request.form["username"]
    password = request.form["password"]

    if users.verify_user(username, password):
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
    
    users.create_user(username,password)

    session["username"] = username
    print(session)
    return redirect("/")

@app.route("/posts/<int:id>")
def show_post(id):
    post,username = discussions.get_post(id)
    post_comments = comments.get_comments(id)
    return render_template("discussion.html", 
                           post=post, 
                           comments=post_comments, 
                           username=username)

@app.route("/posts/<int:id>", methods=["POST"])
def comment_post(id):
    user = session["username"]
    comment = request.form["comment"]
    comments.create_comment(user, id, comment)
    return redirect(f"/posts/{id}")


@app.route("/new")
def new_post():
    return render_template("post_form.html")

@app.route("/create", methods=["POST"])
def create_post():
    found = users.find_user_by_username(session["username"])
    if not found:
        return redirect("/") # ERRORMESSAGE
    title = request.form["title"]
    message = request.form["message"]

    post_id = discussions.create_post(title, message, session["username"])
    
    return redirect(f"/posts/{post_id}")
