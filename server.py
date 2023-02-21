from socket import *
serverPort = 11000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)

print("Server is ready!")
while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    capMessage = message.upper()
    connectionSocket.send(capMessage.encode())
    connectionSocket.close()
