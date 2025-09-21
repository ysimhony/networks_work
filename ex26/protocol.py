"""EX 2.6 protocol implementation
   Author:
   Date:
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820

cmds = ["RAND", "NAME", "TIME", "EXIT"]
def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""

    if data not in cmds:
        return False
    return True


def create_msg(data):
    """Create a valid protocol message, with length field"""
    message = data
    length = str(len(message))
    zfill_length = length.zfill(2)
    message = zfill_length + message
    return message


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length = my_socket.recv(2).decode()

    if not length.isdigit():
        return False, "Error"

    msg = my_socket.recv(int(length)).decode()

    return True, msg
