# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# COPY requirements to /app dir
COPY requirements.txt /app
COPY requirements /app/requirements

RUN export PATH="/app:$PATH"


# Install any needed packages specified in base.txt
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

RUN apt update -y

RUN apt-get install apt-utils libzbar-dev -y
RUN apt-get install libzbar0 -y
