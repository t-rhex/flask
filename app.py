from flask import Flask, render_template, jsonify

# Need to create app now
# Importing class and making an object of the class

app = Flask(__name__)

JOBS = [{
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Benga, India',
    'salary': '$ 120,000'
}, {
    'id': 2,
    'title': 'Software Engineer',
    'location': 'Delhi, India',
    'salary': 'Rs. 12,00,000'
}, {
    'id': 3,
    'title': 'Business Analyst',
    'location': 'Chennai, India'
}, {
    'id': 4,
    'title': 'Intern',
    'location': 'NY, USA',
    'salary': '$60,000'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='Andreew')


@app.route("/api/jobs")
def list_job():
  return jsonify(JOBS)


print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
