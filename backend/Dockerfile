FROM python:3.11.8-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

COPY ./prod-requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN pytest -x -s
