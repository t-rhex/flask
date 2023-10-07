# Use the official Python image as a parent image
FROM python:3.8-alpine

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application files into the container
COPY . /app

# Expose the port on which Gunicorn will run (default is 8000)
EXPOSE 8000

# Define the command to start Gunicorn with your Flask application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
