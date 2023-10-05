from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

db_host = os.environ['DATABASE_HOST']
db_username = os.environ['DATABASE_USERNAME']
db_secret = os.environ['DATABASE_PASSWORD']

connection_string = f"mysql+mysqlconnector://{db_username}:{db_secret}@{db_host}:3306/andrewcareers"
engine = create_engine(connection_string, echo=True)

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


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row._mapping))
    return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
                          {"val": id})
    row = result.fetchone()
    if row is None:
      return None
    else:
      return dict(row._mapping)
