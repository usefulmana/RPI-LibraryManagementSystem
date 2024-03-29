import requests
import time
from google_calendar_service import delete_event


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
    def return_book_from_QR_code(qr_code_data):
        """
        Read the QR code and execute the transaction provided that the QR code is valid
        :param qr_code_data: QR data
        :return: True a condition to break loop
        """

        try:
            qr_data = int(qr_code_data)
            if qr_data > 0:
                # Get the borrow_a_book's information from ID
                req = requests.get(url='http://127.0.0.1:5000/borrow/{}'.format(qr_data))
                # Check if book is already returned
                if req.json()['return_status'] == 'returned':
                    print("[INFO] This book is already returned. Transaction cancelled!")
                    time.sleep(2)
                    return True
                else:
                    # Execute transaction
                    req = requests.put(url='http://127.0.0.1:5000/return/{}'.format(qr_data))
                    if req.json()['event_id'] is not None:
                        delete_event(req.json()['event_id'])
                    print("[INFO] Success!")
                    time.sleep(2)
                    return True
            else:
                print("[INFO] Invalid QR code or no QR code found! Please try again!")
                time.sleep(2)
                return True
        except ValueError:
            print("[INFO] No QR code or QR code contains invalid information! Please try again!")
            time.sleep(2)


if __name__ == '__main__':
    pass