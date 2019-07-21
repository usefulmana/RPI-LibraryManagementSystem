import requests
from borrow_service import BorrowService
import time
from google_calendar_service import delete_event
from routes import get_undue_books_list_of_a_user, return_a_book_route


class ReturnService:
    _instance = None
    @staticmethod
    def get_instance():
        """
        This method will return an instance of ReturnService class
        :return:  An instance of ReturnService class
        """
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
        """
        This function will get the list of undue books of a user
        :param user_email: target user's email
        :param name: target user's name
        :return: a JSON file will include the list of undue books
        """
        user_id = self._borrow_service.get_user_id_from_email(user_email, name)
        req = requests.get(url=get_undue_books_list_of_a_user(user_id))
        res = req.json()
        if "message" in res[0].keys():
            return None
        else:
            return res

    @staticmethod
    def print_list_of_undue_books(res):
        """
        This function will print the list of undue books
        :param res: a JSON file with list of undue books
        :return: none
        """
        book_keys = []
        # Extracting books' ids from the JSON file
        for r in res:
            book_keys.append(r['book_id'])
        books = []
        # Fetch another JSON contains undue books' information
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
    def return_book(user_email, name):
        """
        Displaying the return menu to user
        :param user_email:
        :param name:
        :return: True a condition to break loop
        """
        return_service = ReturnService.get_instance()
        # Getting list of user's undue books
        data = return_service.get_list_of_undue_books(user_email, name)
        if data is None:
            print("You are currently not borrowing any book!")
            print("Returning to main menu...")
            time.sleep(3)
        else:
            return_service.print_list_of_undue_books(data)
            print("Enter an id corresponding to the book u wish to return")
            print("Leave the field blank and press Enter to return main menu")
            try:
                borrow_id = int(input("Your input: ").strip())
                req = requests.put(url=return_a_book_route(borrow_id))
                res = req.json()
                if "message" in res.keys():
                    print("Error: {}".format(res["message"]))
                    print("Returning to main menu...")
                    time.sleep(3)
                else:
                    if res['event_id'] is None:
                        print("Success!")
                        time.sleep(2)
                    else:
                        delete_event(req.json()['event_id'])
                        print("Success!")
                        time.sleep(2)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    service = ReturnService.get_instance()
    service.return_book('fdsa@gmail.com', "bob")
