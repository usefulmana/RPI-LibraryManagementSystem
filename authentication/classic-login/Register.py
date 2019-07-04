from ValidateInput import ValidateInput
import bcrypt


class Register(ValidateInput):
    def register(self):
        username = self.validate_username()
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        password = self.validate_password().encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.curs.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)", (username, first_name, last_name, email, hashed_password,))
        self.conn.commit()
        self.conn.close()
        return "You've successfully registered"
