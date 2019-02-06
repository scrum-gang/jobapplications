from flask import Flask


# app initialization
app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
  return "<h1> Hello World! </h1>"

if __name__ == '__main__':
  app.run()
