#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import subprocess
import sys

import protocol
import glob
import os
import shutil
# import pyautogui

# IP = ????
PHOTO_PATH = r'C:\Networks\work\ex26\screen.jpg' # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    if not protocol.check_cmd(cmd):
        return False, "Error", []


    # Then make sure the params are valid

    # (6)

    words = cmd.split()

    if words[0] == "EXECUTE":
        if not os.path.exists(words[1]):
            return False, "File does not exist", []

    return True, words[0], words[1:]
    # return True, "DIR", ["c:\\cyber"]


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = 'OK'
    print("command: ", command, " params: ", params)
    # (7)
    # "TAKE_SCREENSHOT", "SEND_PHOTO", "DIR", "DELETE", "COPY", "EXECUTE", "EXIT"
    if command == "DIR":
        if len(params) > 0:
            files_list = glob.glob(params[0] + '\*')
        else:
            files_list = glob.glob('\*')
        response = "\n".join(files_list)
    elif command == "COPY":
        shutil.copy(params[0], params[1])
    elif command == "DELETE":
        os.remove(params[0])
    elif command == "EXECUTE":
        subprocess.call(params[0])
    elif command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(r'C:\Networks\work\ex26\screen.jpg')
    elif command == "SEND_PHOTO":
        file_size = os.path.getsize(PHOTO_PATH)
        response = str(file_size)

    return response


def main():
    # open socket with client

    # (1)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)

                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response)


                if command == 'SEND_PHOTO':
                    # Send the data itself to the client
                    # (9)
                    # Read file data
                    with open(PHOTO_PATH, 'rb') as f:
                        file_data = f.read()

                    # Create response: [8-byte file size][file data]
                    # size_header = file_size.to_bytes(8, byteorder='big')
                    print("file data len:", len(file_data))
                    response = file_data
                    client_socket.send(response)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                response = protocol.create_msg(response)
                client_socket.send(response)
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            #send to client
            response = protocol.create_msg(response)
            client_socket.send(response)
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    print(sys.version)
    main()
