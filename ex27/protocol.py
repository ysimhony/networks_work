#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


cmds = ["TAKE_SCREENSHOT", "SEND_PHOTO", "DIR", "DELETE", "COPY", "EXECUTE", "EXIT"]

def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """

    words = data.split()

    if len(words) == 0 or words[0] not in cmds:
        return False

    if words[0] == "TAKE_SCREENSHOT":
        if len(words) > 1:
            return False
    elif words[0] == "SEND_PHOTO":
        """"""
    elif words[0] == "DIR":
        if len(words) > 2:
            return False
    elif words[0] == "DELETE":
        if len(words) != 2:
            return False
    elif words[0] == "COPY":
        if len(words) != 3:
            return False
    elif words[0] == "EXECUTE":
        if len(words) != 2:
            return False
    elif words[0] == "EXIT":
        """"""
    # (3)
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    message = data
    length = str(len(message))
    zfill_length = length.zfill(4)
    message = zfill_length + message

    # (4)
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # (5)

    length = my_socket.recv(4).decode()

    if not length.isdigit():
        return False, "Error"

    msg = my_socket.recv(int(length)).decode()

    return True, msg



