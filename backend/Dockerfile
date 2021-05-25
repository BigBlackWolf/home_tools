FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install -y gcc libssl-dev default-libmysqlclient-dev

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt

ADD . /app/

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "home_tools.wsgi"]


