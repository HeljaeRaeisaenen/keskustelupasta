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
            topic_posts[t.id] = discussions.get_post(t.max)
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

@app.route("/topics/<topic_name>")
def show_topic(topic_name):
    topic_id = topics.get_id(topic_name)
    topic_posts = discussions.get_all_posts(topic_id)
    return render_template("topic.html", topic=topic_name, posts=topic_posts)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = discussions.get_post(post_id)
    post_comments = comments.get_comments(post_id)
    return render_template("discussion.html",
                           post=post,
                           comments=post_comments)


@app.route("/posts/<int:post_id>", methods=["POST"])
def comment_post(post_id):
    user_id = users.find_user_id(session["username"])
    comment = request.form["comment"]
    comments.create_comment(user_id, post_id, comment)
    return redirect(f"/posts/{post_id}")


@app.route("/new")
def new_post():
    topic_s = topics.get_all()
    return render_template("post_form.html", topics=topic_s)


@app.route("/create", methods=["POST"])
def create_post():
    found_user = users.find_user_id(session["username"])
    if not found_user:
        return redirect("/")  # ERRORMESSAGE
    title = request.form["title"]
    message = request.form["message"]
    topic_id = topics.get_id(request.form["topic"])

    post_id = discussions.create_post(title, message, topic_id, found_user)

    return redirect(f"/posts/{post_id}")
