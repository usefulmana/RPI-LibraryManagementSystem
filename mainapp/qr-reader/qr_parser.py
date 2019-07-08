import requests
import ast
import time


class QRParser:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        if QRParser._instance is None:
            QRParser()
        return QRParser._instance

    def __init__(self):
        if QRParser._instance is not None:
            raise Exception("This class is singleton")
        else:
            QRParser._instance = self

    @staticmethod
    def convert_data_to_dict(data):
        try:
            data = ast.literal_eval(data)
        except:
            raise Exception("Invalid data format! JSON only")
        return data

    @staticmethod
    def return_book_from_QR_code(data):
        qr_data = QRParser.get_instance().convert_data_to_dict(data)
        if "borrow_id" not in qr_data.keys():
            print('Invalid QR code!')
        else:
            req = requests.put(url='http://127.0.0.1:5000/return/{}'.format(qr_data['borrow_id']))
            print("Success!")
            time.sleep(2)
