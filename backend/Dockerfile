FROM python:3.11.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY ./prod-requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN pytest -x -s
