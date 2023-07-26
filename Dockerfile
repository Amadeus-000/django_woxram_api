# Use an official Python runtime as a parent image
FROM python:3.8.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install git
RUN apt-get update && apt-get install -y git

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install libmariadb-dev 
RUN apt-get -y install python-dev 
RUN apt-get -y install pkg-config
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Run gunicorn
CMD gunicorn django_woxram_api.wsgi:application --bind 0.0.0.0:8000 -t 300