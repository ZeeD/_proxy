#!/usr/bin/env python3

import socket
import socketserver
import threading


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

    (verb, proxy_path, http_version) = first_row.split(b' ')

    i = proxy_path.index(b'/', proxy_path.index(b'//') + 2)
    (server, server_path) = proxy_path[:i], proxy_path[i:]

    new_row = b' '.join([ verb, server_path, http_version ])

    server_request = b'\r\n'.join([ new_row ] + other_rows)

    return (server, server_request)


def get_local_response(server, request):
    raise Remote()

def get_remote_response(server, request):
    (host, *port) = server[server.index(b'//') + 2:].split(b':')
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

