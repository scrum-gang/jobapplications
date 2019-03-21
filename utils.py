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
db_uri = os.environ.get("DATABASE_URL", "")
if not db_uri:
    db_name = os.environ.get("PSQL_USER", "")
    db_pw = os.environ.get("PSQL_PW", "")
    db_uri = f'postgresql://{db_name}:{db_pw}@localhost/jobapplications'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)

db = SQLAlchemy(app)


def validate_authentication(auth_headers, admin=False):
    if 'Authorization' not in auth_headers:
        return False

    auth_token = auth_headers['Authorization']
    response = query_auth(auth_token)

    # If the token is not verified, it is invalid by default
    if 'verified' not in response:
        return False

    # The request requires admin privileges
    if admin and response['type'] != 'recruiter':
        return False

    return '_id' in response


def query_auth(auth_token):
    """
    Simple wrapper around auth API, re-used in other parts of the code.
    """
    headers = {'content-type': 'application/json', 'Authorization': f"Bearer {auth_token}"}
    return requests.get(f"{auth_base_url}/users/self", headers=headers)
