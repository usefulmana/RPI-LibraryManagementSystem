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
    def check_if_string_is_dict(data):
        if data is None:
            return False
        elif data.startswith('{') and data.endswith('}'):
            return True
        return False

    @staticmethod
    def convert_data_to_dict(data):
        if QRParser.get_instance().check_if_string_is_dict(data):
            return ast.literal_eval(data)
        else:
            return None

    @staticmethod
    def return_book_from_QR_code(qr_code_data):
        qr_data = QRParser.get_instance().convert_data_to_dict(qr_code_data)
        if qr_data is not None:
            if "borrow_id" not in qr_data.keys():
                print('Invalid QR code!')
            else:
                req = requests.get(url='http://127.0.0.1:5000/borrow/{}'.format(qr_data['borrow_id']))
                if req.json()['return_status'] == 'returned':
                    print("This book is already returned. Transaction cancelled!")
                    time.sleep(2)
                    return True
                else:
                    req = requests.put(url='http://127.0.0.1:5000/return/{}'.format(qr_data['borrow_id']))
                    print("Success!")
                    time.sleep(2)
                    return True
        else:
            print("Invalid QR code or no QR code found! Please try scanning again!")
            time.sleep(2)
            return True
