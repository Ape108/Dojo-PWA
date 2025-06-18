# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Run collectstatic to gather all static files into one directory for serving
RUN python manage.py collectstatic --noinput

# Run the app. Gunicorn is a production-grade WSGI server.
# Cloud Run injects the PORT environment variable.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 config.wsgi:application