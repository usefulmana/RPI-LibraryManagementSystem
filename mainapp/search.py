import requests
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

    @staticmethod
    def search_books():
        user_query = input("Please enter a book's title, author, or ISBN: ")
        request = requests.get(url='http://127.0.0.1:5000/books/others/{}'.format(user_query))
        return request.json()

    @staticmethod
    def check_book_exist(id):
        request = requests.get(url='http://127.0.0.1:5000/books/{}'.format(id))
        print(request.json())
        if not request.json():
            return False
        return True
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
            format_string = "{:8s} {:8s} {:45s} {:25s} {:25s} {:20s}"
            print("*********************************************************")
            print(format_string.format("Index", "ID", "Title", "Author", "Published Date(y/m/d)", "ISBN"))
            for r in data:
                print(
                    format_string.format(str(index), str(r["id"]), r["title"], r["author"], r["published_date"], r["ISBN"]))
                index += 1
        else:
            print("No match found. Returning to main menu...")
            return False


if __name__ == '__main__':
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
                ))
                if choice == 1:
                    book_id = input("Enter the ID of the book you'd like to borrow: ")
                    if search.check_book_exist(book_id):
                        print("valid")
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
