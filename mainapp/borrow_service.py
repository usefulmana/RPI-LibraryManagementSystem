import requests
from google_calendar_service import event_insert
from qr_generator import qr_generator
from email_sender import send_email
from routes import add_event_id
from routes import borrow_a_book_route
import time


class BorrowService:
    _instance = None

    @staticmethod
    def get_instance():
        """
        This method returns a singleton BorrowService class
        :return: an instance of BorrowService class
        """
        if BorrowService._instance is None:
            BorrowService()
        return BorrowService._instance

    def __init__(self):
        if BorrowService._instance is not None:
            raise Exception("This class is singleton")
        else:
            BorrowService._instance = self

    @staticmethod
    def borrow_a_book(book_id, user_email, name):
        """
        This methods will execute the POST request to the REST API and provided users additional services...
        :param book_id: id of the book the user want to borrow_a_book
        :param user_email: email of the user who is currently using this application
        :param name: name of the user
        :return: a string to remind of the user of due date
        """
        user_id = BorrowService.get_instance().get_user_id_from_email(user_email, name)
        # Check if user has already borrowed the book and has not returned
        req = requests.post(url=borrow_a_book_route(book_id, user_id))
        res = req.json()
        if "message" in res.keys():
            print("Error: {}".format(res["message"]))
            print("Cancelling transaction...")
            time.sleep(3)
        else:
            g_cal_option = input("Would you like to be reminded of the due date via Google Calendar (Y/n)? ")
            if g_cal_option.strip().upper() == 'Y':
                event_id = event_insert(user_email, book_id, name)
                if event_id is None:
                    print("Not a Gmail account. Calendar services are unavailable!")
                    print("Cancelling transaction...")
                    time.sleep(3)
                else:
                    borrow_id = res['id']
                    BorrowService.get_instance().remind_via_google_calendar(borrow_id, event_id)
            opt_in_qr = input("Would you like to use the Quick Return service (Y/n)? ")
            if opt_in_qr.strip().upper() == 'Y':
                qr_generator(res['id'])
                send_email(user_email)
            print("Success!")
            return "Please return this book before: {}".format(res['due_date'])

    @staticmethod
    def remind_via_google_calendar(borrow_id, event_id):
        requests.put(url=add_event_id(borrow_id, event_id))

    @staticmethod
    def get_user_id_from_email(user_email, name):
        """
        Check if a user already exists in the database. If not, create a new user
        :param user_email: unique identifier for a user
        :param name: name of the user
        :return: id of the user
        """
        req = requests.get('http://127.0.0.1:5000/users/byEmail/{}'.format(user_email))
        if req.json():
            return req.json()['id']
        else:
            data = {"user_email": user_email, "name": name}
            new_user = requests.post(url='http://127.0.0.1:5000/users', json=data)
            return new_user.json()['id']


if __name__ == '__main__':
    print(BorrowService.get_instance().get_user_id_from_email('haha@gmail.com', 'Bob'))
