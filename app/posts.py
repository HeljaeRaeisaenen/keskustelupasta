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
    sql = text("SELECT p.title,p.time,p.id,u.username,c.message,c.time as comment_time FROM posts p "
               "LEFT JOIN users u ON p.user_id=u.id FULL OUTER JOIN comments c ON p.id=c.post_id "
               "WHERE p.topic_id=:id AND (c.id = (select max(id) from comments) "
               "OR NOT EXISTS (select id from comments where post_id=p.id)) "
               "ORDER BY p.id DESC")
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchall()

def delete(post_id):
    db.session.execute(
        text("DELETE FROM posts WHERE id=:id"),
        {"id":post_id})
    db.session.commit()