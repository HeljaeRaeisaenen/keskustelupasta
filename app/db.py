from flask_sqlalchemy import SQLAlchemy
#from dotenv import dotenv_values
from os import getenv
from .app import app

# todo
URI = getenv['DATABASE_URL']

#app.config['SQLALCHEMY_DATABASE_URI'] = URI

app.config["SQLALCHEMY_DATABASE_URI"] = URI.replace("://", "ql://", 1)
db = SQLAlchemy(app)
