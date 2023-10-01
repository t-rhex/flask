from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_jobs_from_db, load_job_from_db, engine, MyModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
from math import ceil

app = Flask(__name__)


# Generate a random job ID
def generate_job_id():
  random_uuid = uuid.uuid4()
  job_code = str(random_uuid).replace('-', '').upper()
  return 'JOB' + job_code[:5]


@app.route("/career")
def hello_world():
  jobs = load_jobs_from_db()
  items_per_page = 10
  total_pages = (len(jobs) + items_per_page - 1) // items_per_page
  return render_template('career_home.html',
                         jobs=jobs,
                         company_name='Andreew',
                         total_pages=total_pages)


@app.route("/career/api/jobs")
def list_job():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/career/api/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  return render_template('job_page_details.html', job=job)


@app.route("/about")
def about():
  return render_template("about.html")


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/career/api/submit_job", methods=['GET'])
def job_form():
  return render_template('job_form.html')


# Route to handle the form submission and save job requirements to the database
@app.route("/career/api/post_job", methods=['POST'])
def post_job():
  job_id = generate_job_id()  # Generate a random job ID
  title = request.form.get('title')
  location = request.form.get('location')
  salary = request.form.get('salary')
  currency = request.form.get('currency')
  responsibilities = request.form.get('responsibilities')
  requirements = request.form.get('requirements')

  # Create a SQLAlchemy session
  Session = sessionmaker(bind=engine)
  session = Session()

  # Create a new job record in the database
  new_job = MyModel(job_id=job_id,
                    title=title,
                    location=location,
                    salary=salary,
                    currency=currency,
                    responsibilities=responsibilities,
                    requirements=requirements)
  session.add(new_job)
  session.commit()

  response_data = {'job_id': new_job.id}
  return jsonify(response_data)

  # # Return the posted job data in the response JSON
  # job_data = {
  #     'job_id': new_job.job_id,
  #     'title': new_job.title,
  #     'location': new_job.location,
  #     'salary': new_job.salary,
  #     'currency': new_job.currency,
  #     'responsibilities': new_job.responsibilities,
  #     'requirements': new_job.requirements
  # }

  # return jsonify(job_data)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
