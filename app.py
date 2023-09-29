from flask import Flask

# Need to create app now
# Importing class and making an object of the class

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "<p>Hello Andrew </p>"


print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
