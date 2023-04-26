from sqlalchemy import text
from .db import db

def create_image(file):
    if not file:
        return None
    data = file.read()
    if len(data) > 100*1024:
        return "Image too large"
    name = file.filename
    sql = text("INSERT INTO images (name, data) VALUES (:name, :data) RETURNING id")
    result = db.session.execute(sql, {"name":name, "data":data})
    img_id = result.fetchone()[0]
    db.session.commit()
    return img_id


def get_by_id(img_id):
    sql = text("SELECT data FROM images WHERE id=:img_id")
    result = db.session.execute(sql, {"img_id":img_id})
    data = result.fetchone()[0]
    return data
