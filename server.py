#!/usr/bin/python

from os import *
from string import *
import socket
from mimetypes import *

server_port = 3000

def get_server_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind(('localhost', port))
    return s

def handle_client(client_msg):
    # 1: parse http GET header to get requested folder/file
    # 2: obtain file listing of folder, or file, as needed
    # 3: interpolate the HTML file and print it to stdout
    print 'Content-Type: text/plain'
    print
    print
    print 'Hi there!'
    return 0


if __name__ == '__main__':
    print 'Starting server...'
    server = get_server_socket(server_port)
    server.listen(5)
    print 'Server is listening on port {0}...'.format(server_port)
    while True:
        (client, address) = server.accept()
        handle_client(client)
