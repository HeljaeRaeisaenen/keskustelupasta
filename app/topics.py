from sqlalchemy import text
from .db import db


def get_all():
    sql = text("SELECT distinct t.id, t.topic, MAX(p.id), COUNT(p.id) FROM topics t"
               " FULL JOIN posts p on p.topic_id=t.id GROUP BY t.id ORDER BY t.id DESC")

    # result has rows containing topic id, max post id inside topic, and n of posts in topic
    result = db.session.execute(sql)
    return result.fetchall()


def get_id(topic_name):
    sql = text("SELECT id FROM topics WHERE topic=:topic")
    result = db.session.execute(sql, {"topic": topic_name})
    return result.fetchone()[0]


def create(topic):
    sql = text("INSERT INTO topics (topic) VALUES (:topic) RETURNING topic")
    result = db.session.execute(sql, {"topic": topic})
    db.session.commit()
    return result.fetchone()[0]


def delete(topic):
    db.session.execute(
        text("DELETE FROM topics WHERE topic=:topic"),
        {"topic": topic}
    )
    db.session.commit()


def search(key):
    result = db.session.execute(
        text("SELECT topic FROM topics WHERE topic LIKE :key"),
        {"key": f"%{key}%"}
    )
    result = result.fetchall()
    unified_result = []
    for row in result:
        unified_result.append(
            {"name": row.topic + " (aihealue)", "link": f"/topics/{row.topic}"})

    return unified_result
