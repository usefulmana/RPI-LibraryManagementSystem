
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

    @staticmethod
    def display_menu(name):
        print('Welcome {}!'.format(name))
        print('Please choose an option')
        print('1. Search books')
        print('2. Borrow a book')
        print('3. Return a book')
        print('4. Log out')
        choice = input("Your choice: ")
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        else:
            print('Invalid input!')


if __name__ == '__main__':
    pass