from flask import render_template, request, redirect, session
from .app import app
from . import users
from . import topics
from . import discussions
from . import comments


@app.route("/")
def index():
    topic_s = topics.get_all()
    topic_posts = {}
    for t in topic_s:
        if not t.max:
            topic_posts[t.id] = None
        else:
            topic_posts[t.id] = discussions.get_post(t.max)[0]
         #post
    return render_template("index.html", topics=topic_s, posts=topic_posts)


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
        return redirect("/")  # ERRORMESSAGE


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
        return redirect("/signup")  # ERRORMESSAGE

    users.create_user(username, password)

    session["username"] = username
    print(session)
    return redirect("/")

@app.route("/topics/<int:topic_id>")
def show_topic(topic_id):
    pass

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post, username = discussions.get_post(post_id)
    post_comments = comments.get_comments(post_id)
    return render_template("discussion.html",
                           post=post,
                           comments=post_comments,
                           username=username)


@app.route("/posts/<int:post_id>", methods=["POST"])
def comment_post(post_id):
    user = session["username"]
    comment = request.form["comment"]
    comments.create_comment(user, post_id, comment)
    return redirect(f"/posts/{post_id}")


@app.route("/new")
def new_post():
    return render_template("post_form.html")


@app.route("/create", methods=["POST"])
def create_post():
    found = users.find_user_by_username(session["username"])
    if not found:
        return redirect("/")  # ERRORMESSAGE
    title = request.form["title"]
    message = request.form["message"]

    post_id = discussions.create_post(title, message, session["username"])

    return redirect(f"/posts/{post_id}")
