from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db


def create_user(username, password):
    passwordhash = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username,passwordhash,admin) VALUES (:username,:passwordhash,false)")
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
    if not user_id:
        return None
    result = db.session.execute(
        text("SELECT username FROM users WHERE id=:id"), {"id": user_id})
    username = result.fetchone()
    if not username:
        print('no usernmae found')
        return None
    return username[0]


def find_user_id(username):
    if not username:
        return False

    result = db.session.execute(
        text("SELECT id FROM users WHERE username=:username"),
        {"username": username})
    user_id = result.fetchone()

    if not user_id:
        print('no user found')
        return None
    return user_id[0]


def is_admin(username):
    result = db.session.execute(
        text("SELECT admin FROM users WHERE username=:username"),
        {"username": username}
    )
    admin = result.fetchone()[0]
    return admin


def get_all():
    result = db.session.execute(
        text("SELECT username FROM users")
    )
    return result.fetchall()


def delete(user):
    user_id = find_user_id(user)
    db.session.execute(
        text("UPDATE posts SET user_id=1 WHERE user_id=:user"),
        {"user": user_id}
    )
    # the idea is that users table, id 1 is reserved for deleted users and when a user is deleted
    # this "user" inherits their posts so the posts can remain but aren't tied to a username
    # this is probably a bad way to do this but i wanted to
    db.session.execute(
        text("UPDATE comments SET user_id=1 WHERE user_id=:user"),
        {"user": user_id}
    )
    db.session.execute(
        text("DELETE FROM users WHERE username=:user"),
        {"user": user}
    )
    db.session.commit()


def search(key):
    result = db.session.execute(
        text("SELECT username FROM users WHERE username LIKE :key"),
        {"key": f"%{key}%"}
    )
    result = result.fetchall()

    unified_result = []
    for row in result:
        unified_result.append(
            {"name": row.username + " (käyttäjä)", "link": f"/user/{row.username}"})

    return unified_result
