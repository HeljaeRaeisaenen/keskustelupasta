import re
from secrets import token_hex
from flask import render_template, request, redirect, session, abort, flash, make_response
from .app import app
from . import users
from . import topics
from . import posts
from . import comments
from . import images


@app.route("/")
def index():
    topic_s = topics.get_all()
    topic_posts = {}
    for topic in topic_s:
        if not topic.max:
            topic_posts[topic.id] = None
        else:
            topic_posts[topic.id] = posts.get_post(topic.max)
    try:
        admin = users.is_admin(session["username"])
    except KeyError:
        admin = False
    return render_template("index.html",
                           topics=topic_s,
                           posts=topic_posts,
                           user_is_admin=admin)


@app.route("/login")
def loginpage():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginaction():
    username = request.form["username"]
    password = request.form["password"]

    if users.verify_user(username, password):
        create_session(username)

        return redirect("/")
    flash("Väärä käyttäjätunnus tai salasana")
    return render_template("login.html")


@app.route("/logout")
def logout_action():
    remove_session()
    return redirect("/")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def sing_up_action():
    username = request.form["username"]
    password = request.form["password"]

    if password != request.form["password_again"]:
        flash("Salasanat eivät olleet samat")
        return redirect("/signup")

    if users.find_user_id(username):
        flash("Käyttäjätunnus on jo käytössä")
        return redirect("/signup")

    stripped = username.strip('\t ')
    if not stripped:
        flash("Käyttäjänimi ei saa olla tyhjä")
        return redirect("/signup")

    users.create_user(username, password)
    create_session(username)

    return redirect("/")


@app.route("/topics/<topic_name>")
def show_topic(topic_name):
    topic_id = topics.get_id(topic_name)
    topic_posts = posts.get_all_posts(topic_id)
    return render_template("topic.html",
                           topic=topic_name,
                           posts=topic_posts,
                           session=session)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    post_comments = comments.get_comments(post_id)
    img = images.get_by_post_id(post_id)

    return render_template("discussion.html",
                           post=post,
                           comments=post_comments,
                           img=img,
                           session=session,
                           user_is_admin=check_admin())


@app.route("/showimage/<int:img_id>")
def show_image(img_id):
    data = images.get_by_id(img_id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/posts/<int:post_id>", methods=["POST"])
def comment_post(post_id):
    check_csrf(request.form["csrf_token"])

    user_id = users.find_user_id(session["username"])
    if not user_id:  # commenting user doesn't exist
        abort(403)
    comment = request.form["comment"]
    # this is because html and python disagree on string len
    comment = re.sub(r'\r\n', '', comment)
    if len(comment) > 5000:
        flash(f"Kommentti oli liian pitkä :( {len(comment)}")
        return redirect(f"/posts/{post_id}")
    if not comment.strip(" \t"):
        flash("Kommentti ei saa olla tyhjä")
        return redirect(f"/posts/{post_id}")
    comments.create_comment(user_id, post_id, comment)
    return redirect(f"/posts/{post_id}")


@app.route("/new")
def new_post():
    topic_s = topics.get_all()
    return render_template("post_form.html", topics=topic_s, session=session)


@app.route("/create", methods=["POST"])
def create_post():
    check_csrf(request.form["csrf_token"])

    found_user = users.find_user_id(session["username"])
    if not found_user:
        abort(403)
    title = request.form["title"]
    message = request.form["message"]
    topic_id = topics.get_id(request.form["topic"])

    if len(title) > 75:
        flash("Otsikko oli liian pitkä")
        return redirect("/new")
    if not title.strip("\t "):
        flash("Otsikko ei saa olla tyhjä")
        return redirect("/new")
    message = re.sub(r'\r\n', '', message)
    if len(message) > 5000:
        flash("Viesti oli liian pitkä")
        return redirect("/new")
    post_id = posts.create_post(title, message, topic_id, found_user)

    img = request.files["img"]
    result = images.create_image(img, post_id)

    if result == "Image too large":
        flash("Kuva oli liian iso. Se saa olla max. 100 kt")
        return redirect("/new")

    return redirect(f"/posts/{post_id}")


@app.route("/newtopic", methods=["POST"])
def create_topic():
    check_csrf(request.form["csrf_token"])
    if not check_admin():
        abort(403)
    topic = request.form["newtopic"]
    if not topic.strip('\t '):
        flash("Aihealueen nimi ei saa olla tyhjä")
        redirect("/adminpage")
    created = topics.create(topic)
    return redirect(f"/topics/{created}")


@app.route("/adminpage")
def adminpage():
    if not check_admin():
        abort(403)
    user_s = users.get_all()
    topic_s = topics.get_all()
    return render_template("adminpage.html", users=user_s, topics=topic_s)


@app.route("/user/<username>")
def userpage(username):
    if not session:
        return render_template("user_page.html", not_logged_in=True)
    if username == "deleted user":
        abort(404)
    user_posts = posts.get_by_user(users.find_user_id(username))
    return render_template("user_page.html",
                           user_posts=user_posts,
                           username=username)


@app.route("/deleteuser", methods=["POST"])
def delete_user():
    check_csrf(request.form["csrf_token"])
    user = request.form["todelete"]

    if user == session["username"]:
        if check_admin():
            flash("Ylläpitäjätunnuksia ei voi poistaa")
            return redirect("/")
        remove_session()
        users.delete(user)
        return redirect("/")
    if not check_admin():
        abort(403)

    if user == 'deleted user':
        abort(403)
    users.delete(user)
    return redirect("/adminpage")


@app.route("/deletetopic", methods=["POST"])
def delete_topic():
    check_csrf(request.form["csrf_token"])
    if not check_admin():
        abort(403)

    topic = request.form["todelete"]
    topics.delete(topic)
    return redirect("/adminpage")


@app.route("/deletepost", methods=["POST"])
def delete_post():
    check_csrf(request.form["csrf_token"])
    posts.delete(request.form["post_to_delete"])
    return redirect(request.form["to_redirect"])


@app.route("/deletecomment", methods=["POST"])
def delete_comment():
    check_csrf(request.form["csrf_token"])
    comments.delete(request.form["comm_to_delete"])
    return redirect(request.form["to_redirect"])


@app.route("/search")
def search_site():
    return render_template("search_page.html")


@app.route("/search", methods=["POST"])
def search_site_result():
    result = []
    search_items = request.form["search_items"]
    keyword = request.form["keyword"]
    if search_items == "topics":
        result += topics.search(keyword)
    elif search_items == "posts":
        result += posts.search(keyword)
    elif search_items == "users":
        result += users.search(keyword)
    else:
        result += topics.search(keyword)
        result += posts.search(keyword)
        result += users.search(keyword)

    if len(result) == 0:
        result.append({"name": "Mitään ei löytynyt"})

    return render_template("search_page.html", result=result)

#################################################################
# helpers


def create_session(username):
    session["username"] = username
    session["csrf_token"] = token_hex(16)


def remove_session():
    del session["username"]
    del session["csrf_token"]


def check_csrf(token):
    if session["csrf_token"] != token:
        abort(403)


def check_admin():
    if len(session) == 0:
        return False
    if users.is_admin(session["username"]):
        return True
    return False
