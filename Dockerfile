FROM python:3.8
MAINTAINER "szhu1017"

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 9091
