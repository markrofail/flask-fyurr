# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements*.txt /code/
RUN pip install -r requirements-dev.txt

# copy project
COPY . /code/
RUN chmod +x ./entrypoint.sh

EXPOSE 8080
