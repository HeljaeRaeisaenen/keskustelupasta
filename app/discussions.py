from db import db
from sqlalchemy import text
from users import find_user_by_username, find_user_by_id

def create_post(title, message, user):
    user_id = find_user_by_username(user)
    sql = text("INSERT INTO posts (title,message,time,user_id) VALUES (:title,:message,NOW(),:user_id) RETURNING id")
    result = db.session.execute(sql, {"title":title, "message":message, "user_id":user_id})
    post_id = result.fetchone()[0]
    db.session.commit()

    return post_id

def get_post(post_id):
    sql = text("SELECT * FROM posts WHERE id=:id")
    result = db.session.execute(sql, {"id":post_id})
    post = result.fetchone()
    username = find_user_by_id(post.user_id)
    return post,username

def get_all_posts():
    result = db.session.execute(text("SELECT title,time,id FROM posts"))
    return result.fetchall()