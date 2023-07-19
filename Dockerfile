# Use an official Python runtime as a parent image
FROM python:3.8.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Run gunicorn
CMD gunicorn django_woxram_api.wsgi:application --bind 0.0.0.0:8000