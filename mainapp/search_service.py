import requests
from borrow import BorrowService
import time
from speech_recognizer import SpeechRecognizer
from return_service import ReturnService


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
            request = requests.get(url='http://127.0.0.1:5000/books')
        else:
            request = requests.get(url='http://127.0.0.1:5000/books/others/{}'.format(user_query.strip()))
        return request.json()

    @staticmethod
    def check_book_exist(id):
        """
        Checking if the book's id user entered exists
        :param id: id of the book
        :return: None if JSON is empty or return a JSON file with the target book's information
        """
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
        """
        Print out the a list of books
        :param data: a JSON file containing a list of books
        :return: False to break the loop
        """
        if data:
            # Added a counter for ease of use
            index = 1
            format_string = "{:3s} {:8s} {:45s} {:25s} {:25s} {:20s}"
            print("*********************************************************")
            print(format_string.format("", "ID", "Title", "Author", "Published Date(y/m/d)", "ISBN"))
            for r in data:
                print(
                    format_string.format(str(index), str(r["id"]), r["title"], r["author"], r["published_date"],
                                         r["ISBN"]))
                index += 1
        else:
            # If there is no match, return False to break loop to return to main menu
            print("No match found. Returning to main menu...")
            return False

    def confirmation(self, data, user_email, name):
        """
        To confirm that the user wants to borrow this book
        :param data: JSON file containing a lists of books
        :param user_email: user's email
        :param name: user's name
        :return: none
        """
        print("You would like to borrow: {} by {}. ISBN: {}".format(data['title'], data['author'], data['ISBN']))
        choice = input("Is this correct (Y/n)? ").strip()
        if choice.upper() == 'Y':
            # Execute transaction if user's said Yes
            print(self._borrow_service.borrow(data['id'], user_email, name))
            print("Success!")
            time.sleep(3)
        else:
            print('Cancelling transaction...')
            time.sleep(2)

    @staticmethod
    def check_if_user_already_borrowed(user_email, name, book_id):
        undue_books_list = ReturnService.get_instance().get_list_of_undue_books(user_email, name)
        # return True if user already borrowed this book and have not returned
        if any(book_id == book['book_id'] for book in undue_books_list):
            return True
        else:
            return False

    @staticmethod
    def display_search_menu(user_email, name):
        """
        Displaying the search and borrow menu
        :param user_email: user's email
        :param name: user's name
        :return: none
        """
        # Initialize an instance of Search class
        search = Search.get_instance()
        while True:
            # Ask user for input
            print("Please enter enter a book's title, author, or ISBN ")
            print("Leave blank and press Enter to view all books")
            user_query = input("Your input: ")
            result = search.search_books(user_query.strip())
            # If print functions return false, meaning no book matched the criteria => break loops
            if search.print_results(result) == False:
                break
            else:
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
                            # If the id entered is correct, proceed to confirmation
                            if search.check_book_exist(
                                    book_id) is not None and not search.check_if_user_already_borrowed(
                                    user_email, name, book_id):
                                search.confirmation(search.check_book_exist(book_id), user_email, name)
                                break
                            elif search.check_if_user_already_borrowed(user_email, name, book_id):
                                print(
                                    "You have already borrowed this book, and have not returned it.\n"
                                    "Transaction cancelled")
                                time.sleep(2)
                                break
                            else:
                                # Return to main menu
                                print("ID is invalid!")
                                break
                        except ValueError:
                            print('Wrong value enter! Numbers only')
                    else:
                        print("Returning to main menu...")
                        time.sleep(2)
                        break
                except Exception as e:
                    print(e)

    @staticmethod
    def search_by_voice(user_email, name):
        search = Search.get_instance()
        text = SpeechRecognizer.get_instance().record_and_decipher_audio()
        while True:
            if text is None:
                break
            else:
                result = search.search_books(text)
                # If print functions return false, meaning no book matched the criteria => break loops
                if search.print_results(result) == False:
                    break
                else:
                    try:
                        print("Choose an option")
                        # Provide user with options to keep going or return to main menu
                        choice = int(input(
                            "1. Borrow a book" + "\n"
                                                 "2. Return to main menu" + "\n"
                                                                            "Your choice: "
                        ).strip())
                        if choice == 1:
                            book_id = input("Enter the ID of the book you'd like to borrow: ").strip()
                            # If the id entered is correct, proceed to confirmation
                            if search.check_book_exist(
                                    book_id) is not None and not search.check_if_user_already_borrowed(
                                    user_email, name, book_id):
                                search.confirmation(search.check_book_exist(book_id), user_email, name)
                                break
                            elif search.check_if_user_already_borrowed(user_email, name, book_id):
                                print(
                                    "You have already borrowed this book, and have not returned it.\n "
                                    "Transaction cancelled")
                                time.sleep(2)
                                break
                            else:
                                # Return to main menu
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
    print(search.check_if_user_already_borrowed("nlbasni2010@gmail.com", "Alex", "1"))
