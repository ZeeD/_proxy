#!/usr/bin/env python3

import socketserver

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
#     server = ThreadedTCPServer(('localhost', 9999), RequestHandler)
#     threading.Thread(target=server.serve_forever).start()
    socketserver.TCPServer(('localhost', 9999), RequestHandler).serve_forever()

