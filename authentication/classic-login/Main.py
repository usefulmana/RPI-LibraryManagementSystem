from Login import Login
from Register import Register


class Main(Login, Register):
    def homepage(self):
        while True:
            option = input("Type L for Login, R for Register: ")
            if option == "L":
                self.login()
                break
            elif option == "R":
                self.register()
                break
            print("Wrong input. Please try again!")


main = Main("pi", "rmit", "iot_a2")
main.homepage()
