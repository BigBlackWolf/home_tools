# Home tools

Project for automation home exercises 

[![Build Status](https://travis-ci.org/BigBlackWolf/home_tools.svg?branch=main)](https://travis-ci.org/BigBlackWolf/home_tools)
[![Coverage Status](https://coveralls.io/repos/github/BigBlackWolf/home_tools/badge.svg)](https://coveralls.io/github/BigBlackWolf/home_tools)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Requirements

- Mysql 8.0.23
- Python 3.8.2

## Installation


- Install packages
```shell
sudo apt-get install python3-dev libmysqlclient-dev build-essential
```

- Create db
```mysql
CREATE USER 'home_user'@'localhost' IDENTIFIED BY 'home_password';
CREATE DATABASE home_tools;
GRANT ALL PRIVILEGES ON *.* TO 'home_user'@'localhost';
```

- Install dependencies
```shell
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
```
