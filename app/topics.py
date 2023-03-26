from sqlalchemy import text
from .db import db


def get_all():
    sql = text("SELECT distinct t.id, t.topic, MAX(p.id), COUNT(p.id) FROM topics t"
               " FULL JOIN posts p on p.topic_id=t.id GROUP BY t.id ORDER BY t.id DESC")

    # result has rows containing topic id, max post id inside topic, and n of posts in topic
    result = db.session.execute(sql)
    return result.fetchall()

# select t.topic, p.id, p.title from topics t inner join posts p on t.id=p.topic_id order by p.id desc;

# "SELECT * FROM topics ORDER BY id DESC UNION SELCT max(id) FROM posts where "


def get_id(topic_name):
    sql = text("SELECT id FROM topics WHERE topic=:topic")
    result = db.session.execute(sql, {"topic": topic_name})
    return result.fetchone()[0]

def create(topic):
    sql = text("INSERT INTO topics (topic) VALUES (:topic) RETURNING topic")
    result = db.session.execute(sql, {"topic":topic})
    db.session.commit()
    return result.fetchone()[0]

def delete(topic):
    result = db.session.execute(
        text("DELETE FROM topics WHERE topic=:topic"),
        {"topic":topic}
    )
    db.session.commit()