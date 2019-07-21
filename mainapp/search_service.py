import requests
from borrow_service import BorrowService
import time
from speech_recognizer import SpeechRecognizer
from routes import get_all_books, get_books_by_search_query, get_book_by_id


class Search:
    _instance = None

    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        """
        This method will return an instance of Search class
        :return: An instance of Search class
        """
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
    def search_books(user_query):
        """
        Take user input and find books in the library within given criteria
        :return: A JSON with a list of books which match the criteria
        """
        if user_query == '':
            request = requests.get(url=get_all_books())
        else:
            request = requests.get(url=get_books_by_search_query(user_query.strip()))
        return request.json()

    @staticmethod
    def check_book_exist(book_id):
        """
        Checking if the book's id user entered exists
        :param book_id: id of the book
        :return: None if JSON is empty or return a JSON file with the target book's information
        """
        res = requests.get(url=get_book_by_id(book_id)).json()
        if "message" in res.keys():
            return None
        else:
            return res

    @staticmethod
    def print_results(data):
        """
        Print out the a list of books
        :param data: a JSON file containing a list of books
        :return: False to break the loop
        """
        # Added a counter for ease of use
        index = 1
        format_string = "{:3s} {:8s} {:45s} {:25s} {:25s} {:20s} {:20s}"
        print("*********************************************************")
        print(format_string.format("", "ID", "Title", "Author", "Published Date(y/m/d)", "ISBN", "Status"))
        for r in data:
            if r['quantity'] != 0:
                print(
                    format_string.format(str(index), str(r["id"]), r["title"], r["author"], r["published_date"],
                                         r["ISBN"], "In stock"))
                index += 1
            else:
                print(
                    format_string.format(str(index), str(r["id"]), r["title"], r["author"], r["published_date"],
                                         r["ISBN"], "Out of stock"))
                index += 1

    def confirmation(self, data, user_email, name):
        """
        To confirm that the user wants to borrow_a_book this book
        :param data: JSON file containing a lists of books
        :param user_email: user's email
        :param name: user's name
        :return: none
        """
        print("You would like to borrow: {} by {}. ISBN: {}".format(data['title'], data['author'], data['ISBN']))
        choice = input("Is this correct (Y/n)? ").strip()
        if choice.upper() == 'Y':
            # Execute transaction if user's said Yes

            self._borrow_service.borrow_a_book(data['id'], user_email, name)
            time.sleep(3)
        else:
            print('Cancelling transaction...')
            time.sleep(2)

    @staticmethod
    def display_search_menu(user_email, name):
        """
        Displaying the search and borrow_a_book menu
        :param user_email: user's email
        :param name: user's name
        :return: none
        """
        # Initialize an instance of Search class
        search = Search.get_instance()
        while True:
            # Ask user for input
            print("Please enter a book's title, author, or ISBN ")
            print("Leave blank and press Enter to view all books")
            user_query = input("Your input: ")
            results = search.search_books(user_query.strip())
            if "message" in results[0].keys():
                print("No matches! Returning to main menu")
                time.sleep(3)
                break
            else:
                search.print_results(results)
                try:
                    print("Choose an option")
                    # Provide user with options to keep going or return to main menu
                    choice = int(input(
                        "1. Borrow a book" + "\n"
                                             "2. Return to main menu" + "\n"
                                                                        "Your choice: "
                    ).strip())
                    if choice == 1:
                        try:
                            book_id = int(input("Enter the ID of the book you'd like to borrow: ").strip())
                            book = search.check_book_exist(book_id)
                            if book is None:
                                print("Book ID does not exist! Returning to main menu...")
                                time.sleep(3)
                                break
                            else:
                                search.confirmation(book, user_email, name)
                                break
                        except ValueError as val:
                            print(val)
                    else:
                        print("Returning to main menu...")
                        time.sleep(2)
                        break
                except Exception as e:
                    print(e)

    @staticmethod
    def search_by_voice(user_email, name):
        text = SpeechRecognizer.get_instance().record_and_decipher_audio()
        while True:
            if text is None:
                break
            else:
                search = Search.get_instance()
                while True:
                    # Ask user for input
                    print("Please enter a book's title, author, or ISBN ")
                    print("Leave blank and press Enter to view all books")
                    results = search.search_books(text.strip())
                    if "message" in results[0].keys():
                        print("No matches! Returning to main menu")
                        time.sleep(3)
                        break
                    else:
                        search.print_results(results)
                        try:
                            print("Choose an option")
                            # Provide user with options to keep going or return to main menu
                            choice = int(input(
                                "1. Borrow a book" + "\n"
                                                     "2. Return to main menu" + "\n"
                                                                                "Your choice: "
                            ).strip())
                            if choice == 1:
                                try:
                                    book_id = int(input("Enter the ID of the book you'd like to borrow: ").strip())
                                    book = search.check_book_exist(book_id)
                                    if book is None:
                                        print("Book ID does not exist! Returning to main menu...")
                                        time.sleep(3)
                                        break
                                    else:
                                        search.confirmation(book, user_email, name)
                                except ValueError as val:
                                    print(val)
                            else:
                                print("Returning to main menu...")
                                time.sleep(2)
                                break
                        except Exception as e:
                            print(e)


if __name__ == '__main__':
    search = Search.get_instance()
    search.display_search_menu('fdsa@gmail.com', "bob")
