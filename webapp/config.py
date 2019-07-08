import json

with open('config.json') as config:
    data = json.load(config)
DEBUG = True
HOST = data['host']
USER = data['user']
PASSWORD = data['password']
DATABASE = data['database']
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
BASIC_AUTH_USERNAME = 'rmit'
BASIC_AUTH_PASSWORD = '123456'
SECRET_KEY = 'secret'
SEND_FILE_MAX_AGE_DEFAULT = 0