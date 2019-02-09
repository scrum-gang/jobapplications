from sqlalchemy import create_engine, exc
import tables
import os
from utils import db

"""
This simple script takes care of the psql set-up.
TODO: Replace this with SQLAlchemy to allow easy migrations.
"""
db_name = os.environ.get("PSQL_USER", "")
db_pw = os.environ.get("PSQL_PW", "")
engine = create_engine(f"postgres://{db_name}:{db_pw}@localhost/jobapplications")
conn = engine.connect()
conn.execute("COMMIT")
try:
    conn.execute("CREATE DATABASE jobapplications")
except exc.ProgrammingError:
    print("exists")
conn.close()

db.create_all()

