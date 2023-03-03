from socket import *
from select import *
from errno import *
import sys

HEADER_LENGTH = 10
PORT = 11000

user = input("Please enter name to join server: ")
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('', PORT))
client_socket.setblocking(False)

username = user.encode()
username_header = f"{len(username):<{HEADER_LENGTH}}".encode()
client_socket.send(username_header + username)

while True:
    message = input(f"{user} : ")

    if message:
        message = message.encode()
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection clossed by server")
                sys.exit()

            username_length = int(username_header.decode())
            username = client_socket.recv(username_length).decode()

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode().strip())
            message = client_socket.recv(message_length).decode()

            print(f"{username} : {message}")

    except IOError as e:
        if e.errno != EAGAIN and e.errno != EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue
