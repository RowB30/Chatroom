from socket import *

close = False

while close == False:
    serverAddress = '', 11000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(serverAddress)

    clientName = input("Enter your name to join the server: ")
    clientSocket.send(clientName.encode())
    message = input()
    newMessage = clientSocket.recv(1024)

    print(f"From server: {newMessage.decode()}")
    if message == "end":
        close = True
