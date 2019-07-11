#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, socket_utils, MySQLdb

HOST = "192.168.1.114"
# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 64000         # The port used by the server.
ADDRESS = (HOST, PORT)
conn = MySQLdb.connect('localhost', 'pi', 'rmit', 'iot_a2')
curs = conn.cursor()


def get_user(user_email):
    curs.execute("SELECT email, first_name, status FROM library_users WHERE email=%s", (user_email,))
    row = curs.fetchone()
    return {"user_email": row[0], "name": row[1], "status": row[2]}


def socket_client(user_email):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        user = get_user(user_email)
        print("Logging in as {}".format(user_email))
        socket_utils.sendJson(s, user)
        while True:
            obj = socket_utils.recvJson(s)
            if obj["status"] == "logged out":
                print("Logging out ...")
                curs.execute("UPDATE library_users SET status=%s WHERE email=%s", ("logged out", user_email))
                conn.commit()
                print("{} has logged out".format(user_email))
                break
