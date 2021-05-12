FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install -y gcc libssl-dev default-libmysqlclient-dev

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt

ADD . /app/



