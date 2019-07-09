from search_service import Search
from return_service import ReturnService
import time
import socket, socket_utils
from config_parser import Parser
from qr_scanner import QRScanner
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
HOST = Parser.get_instance().host
PORT = Parser.get_instance().port
ADDRESS = (HOST, PORT)


class Menu:
    _instance = None
    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        """
        This method returns a singleton Menu class
        :return: an instance of Menu class
        """
        if Menu._instance is None:
            Menu()
        return Menu._instance

    def __init__(self):
        if Menu._instance is not None:
            raise Exception("This class is singleton")
        else:
            Menu._instance = self
            self._qr_scanner = QRScanner.get_instance()
            self._search_service = Search.get_instance()
            self._return_service = ReturnService.get_instance()

    def display_menu(self, name, user_email):
        """
        This methods displays the main menu to users
        :param name: name of user received from Reception Pi
        :param user_email: email of user received from Reception Pi
        :return: none
        """
        while True:
            try:
                print('Welcome {}!'.format(name))
                print('Please choose an option')
                print('1. Search books')
                print('2. Borrow a book')
                print('3. Return a book')
                print('4. Quick Return (QR)')
                print('5. Voice Search')
                print('6. Log out')
                choice = int(input("Your choice: ").strip())
                if choice == 1:
                    self._search_service.display_search_menu(user_email, name)
                elif choice == 2:
                    self._search_service.display_search_menu(user_email, name)
                elif choice == 3:
                    if not self._return_service.return_book(user_email, name):
                        break
                elif choice == 4:
                    self._qr_scanner.scan_qr()
                elif choice == 5:
                    pass
                elif choice == 6:
                    break
                else:
                    print('Invalid Input!')
                    time.sleep(2)
            except Exception as e:
                print(e)
                time.sleep(2)


if __name__ == '__main__':
    # Opening a socket server and wait for Reception's Pi to respond
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        # Infinite loop to prevent program frond exiting
        while True:
            print("Waiting for Reception Pi...")
            s.listen()
            conn, addr = s.accept()
            print("Connected")
            object = socket_utils.recvJson(conn)
            if("end" in object):
                break
            # Notify users that their information has been received
            print("Received")
            menu = Menu.get_instance()
            # Invoke main menu
            menu.display_menu(object['name'], object['user_email'])
            # Return the user JSON with a changed status to let Reception Pi knows the user wants to log out
            object['status'] = "logged out"
            # print("Sending data back.")
            socket_utils.sendJson(conn, object)