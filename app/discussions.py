from sqlalchemy import text
from .db import db


def create_post(title, message, topic, user):
    sql = text(
        "INSERT INTO posts (title,message,time,user_id,topic_id) VALUES "
        "(:title,:message,NOW(),:user,:topic) RETURNING id")
    result = db.session.execute(
        sql, {"title": title, "message": message, "user": user, "topic": topic})
    post_id = result.fetchone()[0]
    db.session.commit()

    return post_id


def get_post(post_id):
    sql = text("SELECT p.id,p.title,p.message,p.time,u.username,t.topic FROM posts p "
               "INNER JOIN users u ON p.user_id=u.id "
               "INNER JOIN topics t ON p.topic_id=t.id WHERE p.id=:id")
    result = db.session.execute(sql, {"id": post_id})
    post = result.fetchone()
    return post


def get_all_posts(topic_id):
    sql = text("SELECT p.title,p.time,p.id,u.username FROM posts p LEFT JOIN users u "
               "ON p.user_id=u.id WHERE p.topic_id=:id ORDER BY p.id DESC")
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchall()
