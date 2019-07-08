#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, socket_utils, MySQLdb

HOST = "192.168.1.114"
# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 64000         # The port used by the server.
ADDRESS = (HOST, PORT)


def get_user(user_email):
    conn = MySQLdb.connect('localhost', 'pi', 'rmit', 'iot_a2')
    curs = conn.cursor()
    curs.execute("SELECT email, first_name, status FROM library_users WHERE email=%s", user_email)
    row = curs.fetchone()
    return {"user_email": row["email"], "name": row["first_name"], "status": row["status"]}


def socket_client(user_email):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        # while True:
            # message = input("Enter message (blank input to end): ")
            # if(not message):
            #     socket_utils.sendJson(s, { "end": True })
            #     break

        user = get_user(user_email)
        print("Logging in as {}".format(user["user_email"]))
        socket_utils.sendJson(s, user)
        print("Waiting for Master Pi ...")
        while True:
            obj = socket_utils.recvJson(s)
            if obj["status"] == "logged out":
                print("Disconnecting from server")
                break

        # print("Received:")
        # print(obj)
        # print("Disconnecting from server.")
    # print("Done.")
