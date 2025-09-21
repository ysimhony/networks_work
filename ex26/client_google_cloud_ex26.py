"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import sys

import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #################################################################
    # make sure to replace the ip with the correct ip of your router
    #################################################################
    my_socket.connect(("46.120.87.185", 12345)) 

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)


        if valid_cmd:
            # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND")
            # 2. Send it to the server
            # 3. If command is EXIT, break from while loop
            # 4. Get server's response
            # 5. If server's response is valid, print it

            msg = protocol.create_msg(user_input)
            my_socket.send(msg.encode())

            if user_input == "EXIT":
                print("Bye bye...")
                break

            valid_rsp, reply = protocol.get_msg(my_socket)

            if valid_rsp:
                print("Server reply: ", reply)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket


if __name__ == "__main__":
    print(sys.version)
    main()

