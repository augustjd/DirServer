#!/usr/bin/python

from os import *
from string import *
import socket
from mimetypes import *

server_port = 80

default_page_path = './static_page.html'
error_page_path = './404.html'

def print_to_socket(socket, msg):
    sent = 0
    msg = msg + '\n'
    total_length = len(msg)
    while sent < total_length:
        sent += socket.send(msg[sent:])

def get_http_header():
    s = 'HTTP/1.0 200 OK\n'
    # can't do date function without the time library
    s += 'Content-Type: text/html\n'
    #s += 'Content-Length: {1}\n'.format(len(msg))
    s += '\n'
    return s



def print_file_to_socket(socket, file_path):
    try:
        if (file_path.split('.')[-1] == 'html'):
            print 'HTML page requested'
            print_to_socket(socket, get_http_header())

        f = file(file_path)
        for x in f:
            print_to_socket(socket, x.strip())
        return True
    except IOError:
        return False

def get_requested_address(request):
    first_line = request.split('\n')[0].strip()
    print 'First line:', first_line
    first_line_length = len(first_line)
    result = ""
    for x in first_line[4:]: # eat the 'GET '
        if x == ' ':
            break
        result += x
    return result

def get_server_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('localhost', port))
    return s

def handle_client(client, request):
    # 1: parse http GET header to get requested folder/file
    # 2: obtain file listing of folder, or file, as needed
    # 3: interpolate the HTML file and print it to stdout
    requested_path = get_requested_address(request)

    if requested_path == '/':
        print_file_to_socket(client, default_page_path)
    elif not print_file_to_socket(client, '.' + requested_path):
        print_file_to_socket(client, error_page_path)

    client.close()
    return 0


if __name__ == '__main__':
    print 'Starting server...'
    server = get_server_socket(server_port)
    server.listen(5)
    print 'Server is listening on port {0}...'.format(server_port)
    while True:
        (client, address) = server.accept()
        request = client.recv(4096)
        handle_client(client, request)
