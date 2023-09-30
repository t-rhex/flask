from flask import Flask, render_template, jsonify
import uuid
from database import engine
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Define your SQLAlchemy model
Base = declarative_base()


class MyModel(Base):
  __tablename__ = 'jobs'  # Replace 'my_table' with your actual table name

  id = Column(Integer, primary_key=True, autoincrement=True)
  job_id = Column(String(250), nullable=False)
  title = Column(String(250), nullable=False)
  location = Column(String(250), nullable=False)
  salary = Column(Integer)
  currency = Column(String(10))
  responsibilities = Column(String(2000))
  requirements = Column(String(2000))


app = Flask(__name__)


def load_jobs_from_db():
  # Fetch rows from the database
  results = session.query(MyModel).all()

  # Loop through the results and convert them to dictionaries
  result_dicts = []
  for result in results:
    row_dict = {
        column.name: getattr(result, column.name)
        for column in MyModel.__table__.columns
    }
    result_dicts.append(row_dict)

  return result_dicts


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs, company_name='Andreew')


@app.route("/api/jobs")
def list_job():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
