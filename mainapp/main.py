from search_service import Search
from return_service import ReturnService
import time
import socket, pprint, socket_utils
from config_parser import Parser

HOST = Parser.get_instance().host
PORT = Parser.get_instance().port
ADDRESS = (HOST, PORT)


class Menu:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        if Menu._instance is None:
            Menu()
        return Menu._instance

    def __init__(self):
        if Menu._instance is not None:
            raise Exception("This class is singleton")
        else:
            Menu._instance = self
            self._search_service = Search.get_instance()
            self._return_service = ReturnService.get_instance()

    def display_menu(self, name, user_email):
        while True:
            try:
                print('Welcome {}!'.format(name))
                print('Please choose an option')
                print('1. Search books')
                print('2. Borrow a book')
                print('3. Return a book')
                print('4. Log out')
                choice = int(input("Your choice: ").strip())
                if choice == 1:
                    self._search_service.display_search_menu(user_email, name)
                elif choice == 2:
                    self._search_service.display_search_menu(user_email, name)
                elif choice == 3:
                    if not self._return_service.return_book(user_email, name):
                        break
                elif choice == 4:
                    break
                else:
                    print('Invalid Input!')
                    time.sleep(2)
            except Exception as e:
                print(e)
                time.sleep(2)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        while True:
            print("Waiting for Reception Pi...")
            s.listen()
            conn, addr = s.accept()
            print("Connected to {}".format(addr))
            object = socket_utils.recvJson(conn)
            if("end" in object):
                break

            print("Received:")
            pprint.pprint(object)
            menu = Menu.get_instance()
            menu.display_menu(object['name'], object['user_email'])

            object['status'] = "logged out"
            # print("Sending data back.")
            socket_utils.sendJson(conn, object)