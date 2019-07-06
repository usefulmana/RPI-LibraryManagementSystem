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
            self._PORT = configs['port']


    @property
    def host(self):
        return self._HOST

    @property
    def port(self):
        return self._PORT


