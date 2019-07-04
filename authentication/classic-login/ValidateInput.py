import re
import MySQLdb


class ValidateInput:
    def __init__(self, db_username, db_password, database):
        self.conn = MySQLdb.connect("localhost", db_username, db_password, database)
        self.curs = self.conn.cursor()

    def validate_email(self):
        while True:
            self.curs.execute("SELECT email FROM library_users")
            data = self.curs.fetchall()
            email = input("Email: ")
            if not email.endswith("@gmail.com"):
                print("You can only use gmail to register and login")
                continue
            for row in data:
                if row is None:
                    break
                elif email == row[0]:
                    print("This email has already been used to register")
                    email = " "
                    break
            if email == " ":
                continue
            else:
                break
        return email

    def validate_password(self):
        message = """Password must contain at least 8 characters
                Must have at least 1 upper-case letter (A-Z)
                Must have at least 1 lower-case letter (a-z)
                Must have at least 1 number (0-9)
                Must have at least 1 special character (~!@#$%^&*+-_.:;,?<>)
                Password must not contain spaces"""
        print(message)
        while True:
            password = input("Password: ")
            if len(password) < 8 or len(password) > 32 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password) or not re.search("[~!@#$%^&*+-_.:;,?<>]", password) or re.search("\s", password):
                print(message)
                continue
            break
        return password
