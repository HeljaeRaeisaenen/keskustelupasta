from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from .app import app

URI = dotenv_values('.env')['DATABASE_URI']

app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)
