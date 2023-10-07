from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_jobs_from_db, load_job_from_db, engine, MyModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import requests

app = Flask(__name__)


# Generate a random job ID
def generate_job_id():
  random_uuid = uuid.uuid4()
  job_code = str(random_uuid).replace('-', '').upper()
  return 'JOB' + job_code[:5]


@app.route("/career")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('job/career_home.html',
                         jobs=jobs,
                         company_name='Andreew')


@app.route("/career/api/jobs")
def list_job():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/career/api/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  return render_template('job/job_page_details.html', job=job)


@app.route("/career/api/submit_job", methods=['GET'])
def job_form():
  return render_template('job/job_form.html')


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

# GraphQL query to pull blog posts from Hashnode
graphql_query = """
{
  user(username: "andrewadhikari") {
    publication {
      posts(page: 0) {
        slug
        title
        brief
        coverImage
        readTime
        dateAdded
      }
      description
    }
    username
    photo
  }
}
"""


# Function to fetch recent posts
@app.route('/api/recent_posts', methods=['GET'])
def fetch_recent_posts():
  try:
    response = requests.post('https://api.hashnode.com/',
                             json={'query': graphql_query})

    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()
    user_data = data.get('data', {}).get('user',
                                         {'username': 'andrewadhikari'})

    posts = user_data.get('publication', {}).get('posts', [])
    description = user_data.get('publication', {}).get('description', '')
    username = user_data.get('username', '')
    photo = user_data.get('photo', '')

    # Limit to the 3 most recent posts
    recent_posts = posts[:3]

    return {
        'description': description,
        'username': username,
        'photo': photo,
        'recent_posts': recent_posts,
    }

  except requests.exceptions.RequestException as e:
    logger.error('Request to Hashnode failed: %s', str(e))
    return None
  except Exception as e:
    logger.error('An error occurred: %s', str(e))
    return None


# Define a route to fetch and display the 3 most recent posts
@app.route("/")
def recent_posts():
  user_data = fetch_recent_posts()

  if user_data is not None:
    return render_template('index.html', user_data=user_data)
  else:
    return jsonify({'error': 'Failed to fetch recent posts'})


@app.route("/posts")
def posts():
  posts = fetch_recent_posts()
  return jsonify(posts)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
