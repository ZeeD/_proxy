#!/usr/bin/env python3

import socket
import socketserver
import threading

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        proxy_request = RequestHandler.read_all(self.request)
        server, server_request = RequestHandler.convert_request(proxy_request)
        response_proxy = RequestHandler.send_request_get_response(server,
                                                            server_request)
        RequestHandler.write_all(self.request, response_proxy)

    @staticmethod
    def read_all(socket):
        chunks = []
        while True:
            chunk = socket.recv(4096)
            chunks.append(chunk)
            if len(chunk) < 4096:
                break
        return b''.join(chunks)

    @staticmethod
    def write_all(socket, response_proxy):
        i = 0
        while True:
            rest = response_proxy[i:]
            if not len(rest):
                break
            i = socket.send(rest)

    @staticmethod
    def convert_request(proxy_request):
        rows = proxy_request.split(b'\r\n')
        first_row, other_rows = rows[0], rows[1:]

        (verb, proxy_path, http_version) = first_row.split(b' ')

        i = proxy_path.index(b'/', proxy_path.index(b'//') + 2)
        (server, server_path) = proxy_path[:i], proxy_path[i:]

        new_row = b' '.join([ verb, server_path, http_version ])

        server_request = b'\r\n'.join([ new_row ] + other_rows)

        return (server, server_request)

    @staticmethod
    def send_request_get_response(server, request):
        (host, *port) = server[server.index(b'//') + 2:].split(b':')
        if port:
            port = int(port[0])
        else:
            port = 80
        with socket.create_connection((host, port)) as conn:
            RequestHandler.write_all(conn, request)
            return RequestHandler.read_all(conn)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer(('localhost', 9999), RequestHandler)
    threading.Thread(target=server.serve_forever).start()

