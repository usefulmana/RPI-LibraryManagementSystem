import requests
from borrow import BorrowService
import time


class ReturnService:
    _instance = None
    @staticmethod
    def get_instance():
        if ReturnService._instance is None:
            ReturnService()
        return ReturnService._instance

    def __init__(self):
        if ReturnService._instance is not None:
            raise Exception("This class is singleton")
        else:
            ReturnService._instance = self
            self._borrow_service = BorrowService.get_instance()

    def get_list_of_undue_books(self, user_email, name):
        user_id = self._borrow_service.get_user_id_from_email(user_email, name)
        req = requests.get(url='http://127.0.0.1:5000/borrow/user/{}'.format(user_id))
        return req.json()

    @staticmethod
    def print_list_of_undue_books(res):
        book_keys = []
        for r in res:
            book_keys.append(r['book_id'])
        books = []
        for i in book_keys:
            req = requests.get(url='http://127.0.0.1:5000/books/{}'.format(i))
            books.append(req.json())
        format_string = "{:3s} {:10s} {:25s} {:45s} {:25s}"
        print('**********************************************')
        print('                 Undue Books                  ')
        print(format_string.format("", "id", "Borrow Date", "Title", "ISBN"))
        index = 1
        for i in range(len(books)):
            print(format_string.format(str(index), str(res[i]['id']), res[i]['borrow_date'], books[i]['title'],
                                       books[i]['ISBN']))
            index += 1

    @staticmethod
    def check_if_book_exist_in_borrow_history(user_input, data):
        for d in data:
            if user_input == d['id']:
                return True
        return False

    def return_book(self, user_email, name):
        return_service = ReturnService.get_instance()
        data = return_service.get_list_of_undue_books(user_email, name)
        return_service.print_list_of_undue_books(data)
        print("Enter an id corresponding to the book u wish to return")
        print("Leave the field blank and press Enter to return main menu")
        try:
            choice = int(input("Your input: ").strip())
            if return_service.check_if_book_exist_in_borrow_history(choice, data):
                req = requests.put(url='http://127.0.0.1:5000/return/{}'.format(choice))
                print("Success!")
                time.sleep(2)
            else:
                print("No such book exists in your borrow history!")
                time.sleep(2)
        except Exception as e:
            print(e)
        return True


if __name__ == '__main__':
    pass
