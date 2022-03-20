FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
COPY ./src .

RUN apt-get update && apt-get upgrade -y
RUN pip3 install -r requirements.txt