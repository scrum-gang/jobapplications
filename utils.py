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
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

