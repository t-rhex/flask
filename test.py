from sqlalchemy import create_engine, text
import os

db_host = os.environ['DATABASE_HOST']
db_username = os.environ['DATABASE_USERNAME']
db_secret = os.environ['DATABASE_PASSWORD']

connection_string = f"mysql+mysqlconnector://{db_username}:{db_secret}@{db_host}:3306/andrewcareers"
engine = create_engine(connection_string, echo=True)


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row._mapping))
    return jobs
