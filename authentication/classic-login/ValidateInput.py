import re
import MySQLdb


class ValidateInput:
    def __init__(self, db_username, db_password, database):
        self.conn = MySQLdb.connect("localhost", db_username, db_password, database)
        self.curs = self.conn.cursor()

    def validate_username(self):
        while True:
            username = input("Username: ")
            self.curs.execute("SELECT username FROM users")
            data = self.curs.fetchall()
            if re.search("\s", username):
                print("Username should not contain spaces")
                continue
            for row in data:
                if row is None:
                    break
                elif username.lower() == row[0].lower():
                    print("Username already exists")
                    username = " "
            if username == " ":
                continue
            else:
                break
        return username

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
            if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password) or not re.search("[~!@#$%^&*+-_.:;,?<>]", password) or re.search("\s", password):
                print(message)
                continue
            break
        return password
