#!/usr/bin/python

import os
from string import *
import socket
import mimetypes

server_port = 80

default_page_path = './'
error_page_path = './404.html'

stylesheet_path = './main.css'
stylesheet = None #global

try:
    sheet = file(stylesheet_path)
    stylesheet = sheet.read()
    sheet.close()
except:
    print "Failed to load stylesheet from ", stylesheet_path


def print_to_socket(socket, msg):
    sent = 0
    msg = msg
    total_length = len(msg)
    while sent < total_length:
        sent += socket.send(msg[sent:])

def get_http_header(content_type):
    s = 'HTTP/1.0 200 OK\n'
    # can't do date function without the time library
    s += 'Content-Type: {0}\n'.format(content_type)
    #s += 'Content-Length: {1}\n'.format(len(msg))
    s += '\n'
    return s

def get_failed_header(content_type):
    s = 'HTTP/1.0 404 Not Found\n'
    # can't do date function without the time library
    s += 'Content-Type: {0}\n'.format(content_type)
    #s += 'Content-Length: {1}\n'.format(len(msg))
    s += '\n'
    return s

def get_directory_page(dir_path):
    files_to_display = [f for f in os.listdir(dir_path) if f[0] != '.'] 
    # don't show hidden files

    s  = '<html>'
    if stylesheet != None:
        s += '<head><style>'
        s += stylesheet
        s += '</style></head>'

    s += '<body>'
    s += '<h1>{0}</h1>'.format(dir_path)
    s += '<a href="http://localhost" class="folder">../</a>'
    for f in files_to_display:
        file_type = 'file'
        if os.path.isdir(os.path.join(dir_path, f)):
            file_type = 'directory'
            f += '/'
        s += '<a href="{0}" class="{1}">{2}</a>'.format(dir_path+f, file_type, f)
    s += '</body>'
    s += '</html>'
    return s

def print_file_to_socket(socket, file_path):
    try:
        (type, encoding) = mimetypes.guess_type(file_path)
        print type, "page requested..."
        if file_path == error_page_path and file_path != '/favicon.ico':
            print "Error 404: couldn't find", file_path
            #print_to_socket(socket, get_failed_header(type))
        elif type == None: #it's a folder
            print "Folder requested..."
            print_to_socket(socket, get_http_header(type))
            print_to_socket(socket, get_directory_page(file_path))
            return
        else:
            print_to_socket(socket, get_http_header(type))

        f = file(file_path)
        print_to_socket(socket, f.read())
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
