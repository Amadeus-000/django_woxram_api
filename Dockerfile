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
RUN apt-get -y install gcc=4:8.3.0-1
RUN apt-get -y install libmariadb-dev=1:10.3.39-0+deb10u1
RUN apt-get -y install python-dev=2.7.16-1
RUN apt-get -y install pkg-config=0.29-6
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Run gunicorn
CMD gunicorn django_woxram_api.wsgi:application --bind 0.0.0.0:8000 -t 300 --workers 4