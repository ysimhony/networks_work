import socket
from datetime import datetime
import random

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")

while True:
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    length = server_socket.recv(2).decode()
    cmd = server_socket.recv(int(length)).decode()

    if cmd == "EXIT":
        break
    elif cmd == "TIME":
        current_time = datetime.now().time()
        datetime_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        reply = datetime_str

    elif cmd == "WHORU":
        server_name = socket.gethostname()
        reply = server_name
    elif cmd == "RAND":
        num = random.randint(1, 10)
        reply = str(num)
    else:
        print("Wrong protocol")

    data = client_socket.recv(1024).decode()
    print("Client sent: " + data)
    reply = "Hello " + data
    client_socket.send(reply.encode())

client_socket.close()
server_socket.close()