# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
# TO DO: import modules
import re
import socket
import os

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1

DEFAULT_URL = "index.html"
ROOT_DIR = "C:\\Networks\\work\\ex44\\webroot\\webroot\\"
FORBIDDEN_FILES = {"secret.txt", "private/data.json", "config.yaml"}


def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as f:
        file_data = f.read()
    return file_data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response

    # Send response
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    if resource == "favicon.ico":
        filename = ROOT_DIR + "imgs\\" + url
    else:
        filename = ROOT_DIR + url

    if filename.find(os.path.join(ROOT_DIR, "calculate-next")) != -1:
        get_param = filename.split("?")[-1]
        # s = "num=16; other=42"
        number = 4
        match = re.search(r'num=(\d+)', get_param)

        if match:
            number = int(match.group(1))
            print(number)  # 16
        number += 1
        number_str = str(number)
        headers = (
            "HTTP/1.0 200 OK\r\n"
            f"Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(number_str)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        body = bytes(str(number), "utf-8")
        response = headers.encode() + body
        client_socket.sendall(response)
        return

    if not os.path.isfile(filename) and resource != "calculate-next":
        print("File not found: " + filename)
        body = b"404 Not Found"
        headers = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        response = headers.encode() + body
        client_socket.sendall(response)
        return

    if url in FORBIDDEN_FILES:
        body = b"403 Forbidden"
        headers = (
            "HTTP/1.1 403 Forbidden\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        response = headers.encode() + body
        client_socket.sendall(response)
        return

    # TO DO: extract requested file tupe from URL (html, jpg etc)
    filetype = filename.split('.')[-1]

    data = get_file_data(filename)

    if filetype == 'html':
        http_header = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
    elif filetype == 'jpg':
        http_header = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: image/jpeg\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
    elif filetype == 'css':
        http_header = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/css\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
    elif filetype == 'js':
        http_header = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/javascript; charset=UTF-8\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
    elif filetype == 'ico':
        http_header = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: image/x-icon\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

    print(filetype)
    http_response = http_header.encode() + data
    client_socket.send(http_response)

    return

    """
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response

    # TO DO: extract requested file tupe from URL (html, jpg etc)
    if filetype == 'html':
        http_header = # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header = # TO DO: generate proper jpg header
    # TO DO: handle all other headers

    # TO DO: read the data from the file
    data = get_file_data(filename)
    http_response = http_header + data
    client_socket.send(http_response.encode())
    """

def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function

    # Split by spaces
    parts = request.split(' ')

    method = parts[0]
    url = parts[1]
    version = parts[2]

    # Check method
    if method != "GET":
        return False

    # Basic check for HTTP version format: starts with "HTTP/"
    if not version.startswith("HTTP/"):
        return False

    resource = url.strip("/").replace("/", "\\")

    return True, resource

def receive_http_request(client_socket):
    """Read HTTP request from client socket until full headers are received or timeout occurs."""
    # client_socket.settimeout(timeout)
    request_data = ""

    while True:
        try:
            chunk = client_socket.recv(1024).decode()
            request_data += chunk
            if "\r\n\r\n" in request_data:
                # End of headers
                break
        # except socket.timeout:
            # print("Timeout while receiving data.")
        except Exception as e:
            print("Error while receiving data:", e)
            # break


    return request_data

def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    # client_socket.send(FIXED_RESPONSE.encode())
    """
    while True:
        # TO DO: insert code that receives client request
        # ...
        
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    """


    while True:
        client_request = receive_http_request(client_socket)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()