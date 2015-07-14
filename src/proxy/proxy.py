#!/usr/bin/env python3

import socket
import socketserver
import threading
import re

class Remote(Exception):
    pass


def read_all(socket):
    chunks = []
    while True:
        chunk = socket.recv(4096)
        chunks.append(chunk)
        if len(chunk) < 4096:
            break
    return b''.join(chunks)


def write_all(socket, response):
    i = 0
    while True:
        rest = response[i:]
        if not len(rest):
            break
        i = socket.send(rest)


def convert_request(proxy_request):
    rows = proxy_request.split(b'\r\n')
    first_row, other_rows = rows[0], rows[1:]

    verb, proxy_path, http_version = first_row.split(b' ')

    i = proxy_path.index(b'/', proxy_path.index(b'//') + 2)
    server, server_path = proxy_path[:i], proxy_path[i:]

    new_row = b' '.join((verb, server_path, http_version))

    server_request = b'\r\n'.join([new_row] + other_rows)

    return server, server_request


def local_file(fname):
    with open(fname, 'rb') as f:
        return f.read()

LOCAL_RESPONSE_RULES = {
    ('http://skygo.sky.it', '/config/config.min.js'): lambda: local_file(r'C:\Users\DeTullioVito\Desktop\workspace\_Proxy\assets\foo.txt'),
    ('http://skygo-e.sky.it', re.compile('/config/.*')): lambda: local_file(r'C:\Users\DeTullioVito\Desktop\workspace\_Proxy\assets\bar.txt')
}


def eqmatch(str_or_regex, byte_string, regex_type=type(re.compile(''))):
    string = byte_string.decode()
    if isinstance(str_or_regex, str):
        return str_or_regex == string
    if isinstance(str_or_regex, regex_type):
        return str_or_regex.match(string)
    raise Exception()


def enrich_with_headers(body):
    return b'HTTP/1.1 200 OK\r\n\r\n' + body


def get_local_response(server, request):
    request_first_row = request.split(b'\r\n', 1)[0]
    _, server_path, _ = request_first_row.split(b' ', 2)

    for s, p in LOCAL_RESPONSE_RULES:
        if eqmatch(s, server) and eqmatch(p, server_path):
            body = LOCAL_RESPONSE_RULES[(s, p)]()
            return enrich_with_headers(body)

    raise Remote()

def get_remote_response(server, request):
    host, *port = server[server.index(b'//') + 2:].split(b':')
    if port:
        port = int(port[0])
    else:
        port = 80
    with socket.create_connection((host, port)) as conn:
        write_all(conn, request)
        return read_all(conn)


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('handle [request: %r]' % (self.request, ))
        proxy_request = read_all(self.request)
        server, server_request = convert_request(proxy_request)

        try:
            response = get_local_response(server, server_request)
        except Remote:
            response = get_remote_response(server, server_request)

        print('handle [response: %r]' % (response, ))
        write_all(self.request, response)

    
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer(('localhost', 9999), RequestHandler)
    threading.Thread(target=server.serve_forever).start()

