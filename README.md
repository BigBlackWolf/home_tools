# Home tools

Project for automation home exercises 

[![Build Status](https://travis-ci.org/BigBlackWolf/home_tools.svg?branch=main)](https://travis-ci.org/BigBlackWolf/home_tools)
[![Coverage Status](https://coveralls.io/repos/github/BigBlackWolf/home_tools/badge.svg)](https://coveralls.io/github/BigBlackWolf/home_tools)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Requirements

- Mysql 8.0.23
- Python 3.8.2
- VueJs 4.5.12

## Installation

Build images
```shell script
docker-compose build
```

Run db migrations
```shell script
docker-compose run backend python manage.py makemigrations api
docker-compose run backend python manage.py migrate
```

Create admin user
```shell script
docker-compose run app python manage.py createsuperuser
```

Run your app
```shell script
docker-compose up
```


To push Image to dockerhub:

```shell script
docker build -t bigblackwolf/home_tools:backend backend 
docker push bigblackwolf/home_tools:backend
```
