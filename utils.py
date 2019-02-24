from flask import Flask
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import os
import requests

auth_base_url = "https://jobhub-authentication-staging.herokuapp.com"
# app initialization
app = Flask(__name__)
app.debug = True


# Config
db_name = os.environ.get("PSQL_USER", "")
db_pw = os.environ.get("PSQL_PW", "")
db_uri = f'postgresql://{db_name}:{db_pw}@localhost/jobapplications'
heroku_uri = os.environ.get("HEROKU_POSTGRESQL_AMBER_URL", "")
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)

db = SQLAlchemy(app)


def validate_authentication(content, user=None, admin=False):
    if 'auth' not in content:
        return False
    headers = {'content-type': 'application/json', 'Authorization': f"Bearer {content['auth']}"}
    response = requests.get(f"{auth_base_url}/users/self", headers=headers)
    if 'verified' not in response:
        return False

    if admin and response['type'] != 'recruiter':
        return False

    if user:
        return response['_id'] == user
    else:
        return response['verified']
