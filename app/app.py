from flask import Flask
from dotenv import dotenv_values

app = Flask(__name__)
app.secret_key = dotenv_values('.env')['SECRET_KEY']

import routes