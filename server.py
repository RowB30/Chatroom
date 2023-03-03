from socket import *
from select import *

HEADER_LENGTH = 10
PORT = 11000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(5)

sockets_list = [server_socket]

clients = {}


def recieve_message(client_socket):
    try:
        message_headder = client_socket.recv(HEADER_LENGTH)

        if not len(message_headder):
            return False

        message_length = int(message_headder.decode())

        return {"header": message_headder, "data": client_socket.recv(message_length)}
    except:
        return False


print("Server is ready!")
while True:
    read_sockets, _, excetion_sockets = select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = recieve_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"{user['data'].decode()} has joined the chat room.")
        else:
            message = recieve_message(notified_socket)

            if message is False:
                print(
                    f"Closed connection from {clients[notified_socket]['data'].decode()}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"{user['data'].decode()}: {message['data'].decode()}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data'])
