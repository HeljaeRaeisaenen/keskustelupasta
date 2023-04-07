from sqlalchemy import text
from .db import db


def create_comment(user_id, post_id, comment):
    sql = text(
        "INSERT INTO comments (message,time,user_id,post_id) VALUES "
        "(:message, NOW(), :user_id, :post_id)")
    db.session.execute(
        sql, {"message": comment, "user_id": user_id, "post_id": post_id})
    db.session.commit()


def get_comments(post_id):
    sql = "SELECT c.id, c.message, c.time, u.username FROM comments c, users u "\
        "WHERE c.post_id=:id AND c.user_id=u.id ORDER BY c.id"
    result = db.session.execute(text(sql), {"id": post_id})
    comments = result.fetchall()
    return comments


def delete(comm_id):
    db.session.execute(
        text("DELETE FROM comments WHERE id=:id"),
        {"id": comm_id})
    db.session.commit()
