# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y g++ gcc gettext

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.pip /code/requirements.pip
RUN pip install -r requirements.pip

# Copy project
COPY explonary /code/explonary
