from Login import Login
from Register import Register
import time


class Main(Login, Register):
    def homepage(self):
        print("Welcome to Library Management System")
        while True:
            option = input("Type L for Login, R for Register: ")
            if option == "L":
                self.login()
                time.sleep(3)
                continue
            if option == "R":
                self.register()
                time.sleep(3)
                continue
            print("Wrong input. Please try again!")


main = Main("pi", "rmit", "iot_a2")
main.homepage()
