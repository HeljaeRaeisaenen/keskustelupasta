from sqlalchemy import text
from .db import db

def get_all():
    sql = text("SELECT distinct t.id, t.topic, MAX(p.id), COUNT(p.id) FROM topics t"\
               " FULL JOIN posts p on p.topic_id=t.id GROUP BY t.id ORDER BY t.id DESC")

    # result has rows containing topic id, max post id inside topic, and n of posts in topic
    result = db.session.execute(sql)
    return result.fetchall()

#select t.topic, p.id, p.title from topics t inner join posts p on t.id=p.topic_id order by p.id desc;

#"SELECT * FROM topics ORDER BY id DESC UNION SELCT max(id) FROM posts where "