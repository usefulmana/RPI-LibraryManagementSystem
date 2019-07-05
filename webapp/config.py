import json

with open('config.json') as config:
    data = json.load(config)
DEBUG = True
HOST = data['host']
USER = data['user']
PASSWORD = data['password']
DATABASE = data['database']
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
