import requests
import ast
import time


class QRParser:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        """
         This method will return an instance of QRParser class
        :return:  An instance of QRParser class
        """
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
        """
        validate data
        :param data: any but preferably  stringified a JSON or a dictionary
        :return: false if data is empty or not JSON or dictionary,  True if otherwise
        """
        if data is None:
            return False
        elif data.startswith('{') and data.endswith('}'):
            return True
        return False

    @staticmethod
    def convert_data_to_dict(data):
        """
        Converting a stringified JSON into a dictionary
        :param data: stringified JSON
        :return: a dictionary
        """
        # Validate data first before conversion
        if QRParser.get_instance().check_if_string_is_dict(data):
            return ast.literal_eval(data)
        else:
            return None

    @staticmethod
    def return_book_from_QR_code(qr_code_data):
        """
        Read the QR code and execute the transaction provided that the QR code is valid
        :param qr_code_data: QR data
        :return: True a condition to break loop
        """
        # Extract data
        qr_data = QRParser.get_instance().convert_data_to_dict(qr_code_data)
        # If data is not empty
        if qr_data is not None:
            # make sure that data is correct
            if "borrow_id" not in qr_data.keys():
                print('Invalid QR code!')
            else:
                # Get the borrow's information from ID
                req = requests.get(url='http://127.0.0.1:5000/borrow/{}'.format(qr_data['borrow_id']))
                # Check if book is already returned
                if req.json()['return_status'] == 'returned':
                    print("This book is already returned. Transaction cancelled!")
                    time.sleep(2)
                    return True
                else:
                    # Execute transaction
                    req = requests.put(url='http://127.0.0.1:5000/return/{}'.format(qr_data['borrow_id']))
                    print("Success!")
                    time.sleep(2)
                    return True
        else:
            print("Invalid QR code or no QR code found! Please try scanning again!")
            time.sleep(2)
            return True
