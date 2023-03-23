from sqlalchemy import text
from .db import db


def create_comment(user_id, post_id, comment):
    sql = text(
        "INSERT INTO comments (message,time,user_id,post_id) VALUES "\
        "(:message, NOW(), :user_id, :post_id)")
    db.session.execute(
        sql, {"message": comment, "user_id": user_id, "post_id": post_id})
    db.session.commit()


def get_comments(comm_id):
    sql = "SELECT C.message, C.time, U.username FROM comments C, users U WHERE C.post_id=:id "\
        "AND C.user_id=U.id ORDER BY C.id"
    result = db.session.execute(text(sql), {"id": comm_id})
    comments = result.fetchall()
    return comments
