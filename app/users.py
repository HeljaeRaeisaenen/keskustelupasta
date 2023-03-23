from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db


def create_user(username, password):
    passwordhash = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username,passwordhash) VALUES (:username,:passwordhash)")
    db.session.execute(
        sql, {"username": username, "passwordhash": passwordhash})
    db.session.commit()


def verify_user(username, password):
    sql = text("SELECT username,passwordhash FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    existent_user = result.fetchone()
    # print(existent_user)
    if not existent_user:
        return False
    saved_hash = existent_user.passwordhash
    if check_password_hash(saved_hash, password):
        return True
    return False


def find_username(user_id):
    result = db.session.execute(
        text("SELECT username FROM users WHERE id=:id"), {"id": user_id})
    username = result.fetchone()
    if not username:
        print('no usernmae found')
        return None
    return username[0]


def find_user_id(username):
    result = db.session.execute(
        text("SELECT id FROM users WHERE username=:username"), {"username": username})
    user_id = result.fetchone()

    if not user_id:
        print('no user found')
        return None
    return user_id[0]
