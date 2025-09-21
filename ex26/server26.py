"""EX 2.6 server implementation
   Author:
   Date:
"""

import socket
import protocol
import random
from datetime import datetime
import sys



def create_server_rsp(cmd):
    """Based on the command, create a proper response"""

    rsp = ""
    if cmd == "TIME":
        current_datetime = datetime.now()
        datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # current_time = datetime.now().time()
        # datetime_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        rsp = datetime_str
    elif cmd == "NAME":
        server_name = socket.gethostname()
        rsp = server_name
    elif cmd == "RAND":
        num = random.randint(1, 10)
        rsp = str(num)
    # else:
    #     print("Wrong protocol")

    rsp = protocol.create_msg(rsp)
    return rsp


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    #server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            # 2. Check if the command is valid
            # 3. If valid command - create response
            print("client request: ", cmd)
            if protocol.check_cmd(cmd):
                response = create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == "EXIT":
            break

        # Send response to the client
        client_socket.send(response.encode())

    print("Closing\n")
    # Close sockets


if __name__ == "__main__":
    print(sys.version)
    main()
