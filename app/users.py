from db import db
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def create_user(username, password):
    passwordhash = generate_password_hash(password)
    sql = text("INSERT INTO users (username,passwordhash) VALUES (:username,:passwordhash)")
    db.session.execute(sql, {"username":username, "passwordhash":passwordhash})
    db.session.commit()

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

def find_user_by_id(id):
    result = db.session.execute(text("SELECT username FROM users WHERE id=:id"), {"id":id})
    username = result.fetchone()[0]
    return username

def find_user_by_username(username):
    result = db.session.execute(text("SELECT id FROM users WHERE username=:username"), {"username":username})
    id = result.fetchone()[0]
    return id