from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# app initialization
app = Flask(__name__)
app.debug = True


# Config
# TODO [aungur]: this uri might be wrong
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobapplications'


db = SQLAlchemy(app)
