import requests
from borrow import BorrowService
import time


class Search:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        if Search._instance is None:
            Search()
        return Search._instance

    def __init__(self):
        if Search._instance is not None:
            raise Exception("This class is singleton")
        else:
            Search._instance = self
            self._borrow_service = BorrowService.get_instance()

    @staticmethod
    def search_books():
        user_query = input("Please enter a book's title, author, or ISBN: ")
        request = requests.get(url='http://127.0.0.1:5000/books/others/{}'.format(user_query))
        return request.json()

    @staticmethod
    def check_book_exist(id):
        request = requests.get(url='http://127.0.0.1:5000/books/{}'.format(id))
        if not request.json():
            return None
        return request.json()
        # else:
        #     r = request.json()[0]
        #     print("You would like to borrow: {} by {}".format(r['title'], r['author']))
        #     choice = input("Is this correct (Y/n)? ")
        #     if choice.upper() == 'Y':
        #         return True
        #     else:
        #         return False

    @staticmethod
    def print_results(data):
        if data:
            index = 1
            format_string = "{:3s} {:8s} {:45s} {:25s} {:25s} {:20s}"
            print("*********************************************************")
            print(format_string.format("", "ID", "Title", "Author", "Published Date(y/m/d)", "ISBN"))
            for r in data:
                print(
                    format_string.format(str(index), str(r["id"]), r["title"], r["author"], r["published_date"], r["ISBN"]))
                index += 1
        else:
            print("No match found. Returning to main menu...")
            return False

    def confirmation(self, data, user_email, name):
        print("You would like to borrow: {} by {}. ISBN: {}".format(data['title'], data['author'], data['ISBN']))
        choice = input("Is this correct (Y/n)? ").strip()
        if choice.upper() == 'Y':
            print(self._borrow_service.borrow(data['id'], user_email, name))
            print("Success!")
            time.sleep(3)
        else:
            print('Cancelling transaction...')
            time.sleep(2)

    @staticmethod
    def display_search_menu(user_email, name):
        search = Search.get_instance()
        while True:
            result = search.search_books()
            if search.print_results(result) == False:
                break
            else:
                try:
                    print("Choose an option")
                    choice = int(input(
                        "1. Borrow a book" + "\n"
                                             "2. Return to main menu" + "\n"
                                                                        "Your choice: "
                    ).strip())
                    if choice == 1:
                        book_id = input("Enter the ID of the book you'd like to borrow: ").strip()
                        if search.check_book_exist(book_id) is not None:
                            search.confirmation(search.check_book_exist(book_id), user_email, name)
                            break
                        else:
                            print("ID is invalid or does not exist!")
                            break
                    else:
                        print("Returning to main menu...")
                        time.sleep(2)
                        break
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    search = Search.get_instance()
    search.display_search_menu()
