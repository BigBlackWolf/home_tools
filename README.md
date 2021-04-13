# Home tools

Project for automation home exercises 

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
GRANT ALL PRIVILEGES ON home_tools.* TO 'home_user'@'localhost';
```

- Install dependencies
```shell
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
```
