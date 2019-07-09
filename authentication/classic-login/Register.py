from ValidateInput import ValidateInput
import bcrypt, socket_client


class Register(ValidateInput):
    def register(self):
        email = self.validate_email()
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = self.validate_password()
        status = "logged in"
        while True:
            retype_password = input("Retype your password: ")
            if retype_password == password:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                self.curs.execute("INSERT INTO library_users VALUES (%s, %s, %s, %s, %s)", (email, first_name, last_name, hashed_password, status))
                self.conn.commit()
                self.conn.close()
                print("You've successfully registered")
                socket_client.socket_client(email)
                break
            print("Please retype your password correctly")
