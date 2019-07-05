import json


class Parser:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        if Parser._instance is None:
            Parser()
        return Parser._instance

    def __init__(self):
        if Parser._instance is not None:
            raise Exception("This class is singleton")
        else:
            Parser._instance = self
            self._CONFIG = 'config.json'
            with open(self._CONFIG, 'r') as file:
                configs = json.load(file)
            self._HOST = configs['host']
            self._USER = configs['user']
            self._PASSWORD = configs['password']
            self._DATABASE = configs['database']
            self._SECRET = configs["secret_key"]
            self._DAYS_TO_RETURN = configs["days_to_return_book"]

    @property
    def host(self):
        return self._HOST

    @property
    def user(self):
        return self._USER

    @property
    def password(self):
        return self._PASSWORD

    @property
    def database(self):
        return self._DATABASE

    @property
    def days_to_return(self):
        return self._DAYS_TO_RETURN

    @property
    def secret(self):
        return self._SECRET

