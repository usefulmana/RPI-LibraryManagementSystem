import json


class Parser:
    """
    Parsing config file. Nothing of import
    """
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
            self._EMAIL = configs['email']
            self._CALENDAR_REMINDER = configs["days_to_be_reminded"]

    @property
    def host(self):
        return self._HOST

    @property
    def port(self):
        return self._PORT

    @property
    def email(self):
        return self._EMAIL

    @property
    def calendar_reminder(self):
        return self._CALENDAR_REMINDER


