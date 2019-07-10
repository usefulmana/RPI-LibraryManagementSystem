import requests
from google_calendar_service import event_insert
from qr_generator import qr_generator
from email_sender import send_email


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
    def borrow(book_id, user_email, name):
        """
        This methods will execute the POST request to the REST API and provided users additional services...
        :param book_id: id of the book the user want to borrow
        :param user_email: email of the user who is currently using this application
        :param name: name of the user
        :return: a string to remind of the user of due date
        """
        user_id = BorrowService.get_instance().get_user_id_from_email(user_email, name)
        # Check if user has already borrowed the book and has not returned
        req = requests.post('http://127.0.0.1:5000/borrow/{}/user/{}'.format(book_id, user_id))
        choice = input("Would you like to be reminded of the due date via Google Calendar (Y/n)? ")
        if choice.strip().upper() == 'Y':
            new_req = requests.put(
                'http://127.0.0.1:5000/borrow/{}/event/{}'.format(req.json()['id'], event_insert(user_email, book_id, name)))
        opt_in_qr = input("Would you like to use the Quick Return service (Y/n)? ")
        if opt_in_qr.strip().upper() == 'Y':
            qr_generator(req.json()['id'])
            send_email(user_email)
        return "Please return this book before: {}".format(req.json()['due_date'])

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
