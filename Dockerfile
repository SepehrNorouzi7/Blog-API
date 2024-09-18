FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./core/requirements.txt /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

COPY ./core /app/
