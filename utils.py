from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# app initialization
app = Flask(__name__)
app.debug = True


# Config
db_name = os.environ.get("PSQL_USER", "")
db_pw = os.environ.get("PSQL_PW", "")
db_uri = f'postgresql://{db_name}:{db_pw}@localhost/jobapplications'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)
