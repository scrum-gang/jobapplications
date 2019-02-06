from flask import Flask
from sqlalchemy import create_engine

#engine = create_engine('postgresql://localhost:5432/jobapplications')
# app initialization
app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
  return "<h1> Hello World! </h1>"

if __name__ == '__main__':
  app.run()
