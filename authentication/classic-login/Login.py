import bcrypt
import MySQLdb


class Login:
    def __init__(self, db_username, db_password, database):
        self.conn = MySQLdb.connect("localhost", db_username, db_password, database)
        self.curs = self.conn.cursor()

    def login(self):
        while True:
            self.curs.execute("SELECT email, password FROM library_users")
            data = self.curs.fetchall()
            email = input("Email: ")
            password = input("Password: ").encode("utf-8")
            for row in data:
                if email == row[0]:
                    if bcrypt.checkpw(password, row[1].encode()):
                        print("You've successfully logged in")
                        password = " "
                        break
            if password != " ":
                print("Incorrect username or password")
                continue
            else:
                break
