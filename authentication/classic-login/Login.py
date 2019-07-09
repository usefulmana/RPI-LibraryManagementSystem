import bcrypt
import MySQLdb
import socket_client


class Login:
    def __init__(self, db_username, db_password, database):
        self.conn = MySQLdb.connect("localhost", db_username, db_password, database)
        self.curs = self.conn.cursor()

    def login(self):
        while True:
            self.curs.execute("SELECT email, password, status FROM library_users")
            data = self.curs.fetchall()
            email = input("Email: ")
            password = input("Password: ").encode("utf-8")
            status = "logged in"
            backup = 0
            for row in data:
                if email == row[0]:
                    if bcrypt.checkpw(password, row[1].encode()):
                        backup = 1
                    if row[2] != status:
                        status = "logged out"
                    break
            if backup == 0:
                print("Incorrect email or password")
                continue
            elif backup == 1 and status == "logged out":
                print("You've successfully logged in")
                self.curs.execute("UPDATE library_users SET status=%s WHERE email=%s", ("logged in", email))
                self.conn.commit()
                socket_client.socket_client(email)
                break
            elif backup == 1 and status == "logged in":
                print("Someone is currently using this account")
                break
