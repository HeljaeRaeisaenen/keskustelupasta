from db import db
from sqlalchemy import text
from users import find_user_by_username, find_user_by_id

def create_comment(user, post_id, comment):
    user_id = find_user_by_username(user)
    sql = text("INSERT INTO comments (message,time,user_id,post_id) VALUES (:message, NOW(), :user_id, :post_id)")
    db.session.execute(sql, {"message":comment, "user_id":user_id, "post_id":post_id})
    db.session.commit()

def get_comments(id):
    sql = "SELECT C.message, C.time, U.username FROM comments C, users U WHERE C.post_id=:id "\
        "AND C.user_id=U.id ORDER BY C.id"
    result = db.session.execute(text(sql), {"id":id})
    comments = result.fetchall()
    return comments
