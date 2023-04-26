from sqlalchemy import text
from .db import db

def create_image(file, post_id):
    if not file:
        return None
    data = file.read()
    if len(data) > 100*1024:
        return "Image too large"
    name = file.filename
    sql = text("INSERT INTO images (name,data,post_id) VALUES (:name,:data,:post_id)")
    db.session.execute(sql, {"name":name, "data":data, "post_id":post_id})
    db.session.commit()

def get_by_post_id(post_id):
    sql = text("SELECT id,name FROM images WHERE post_id=:post_id")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def get_by_id(img_id):
    sql = text("SELECT data FROM images WHERE id=:img_id")
    result = db.session.execute(sql, {"img_id":img_id})
    data = result.fetchone()[0]
    return data
