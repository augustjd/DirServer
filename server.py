#!/usr/bin/python

from os import *
from string import *
import socket
from mimetypes import *

server_port = 80

def print_to_socket(socket, msg):
    sent = 0
    msg = msg + '\n'
    total_length = len(msg)
    while sent < total_length:
        sent += socket.send(msg[sent:])
        

def get_server_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind(('localhost', port))
    return s

def handle_client(client):
    # 1: parse http GET header to get requested folder/file
    # 2: obtain file listing of folder, or file, as needed
    # 3: interpolate the HTML file and print it to stdout
    print_to_socket(client, 'Hi there!')
    client.close()
    return 0


if __name__ == '__main__':
    print 'Starting server...'
    server = get_server_socket(server_port)
    server.listen(5)
    print 'Server is listening on port {0}...'.format(server_port)
    while True:
        (client, address) = server.accept()
        handle_client(client)
