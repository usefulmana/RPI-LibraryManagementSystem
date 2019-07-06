import requests


class BorrowService:
    _instance = None
    @staticmethod
    def get_instance():
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
        user_id = BorrowService.get_instance().get_user_id_from_email(user_email, name)
        req = requests.post('http://127.0.0.1:5000/borrow/{}/user/{}'.format(book_id, user_id))
        return "Please return this book before: {}".format(req.json()['return_date'])

    @staticmethod
    def get_user_id_from_email(user_email, name):
        req = requests.get('http://127.0.0.1:5000/users/byEmail/{}'.format(user_email))
        if req.json():
            return req.json()['id']
        else:
            data = {"user_email": user_email, "name": name}
            new_user = requests.post(url='http://127.0.0.1:5000/users', json=data)
            return new_user.json()['id']


if __name__ == '__main__':
    print(BorrowService.get_instance().get_user_id_from_email('haha@gmail.com', 'Bob'))
