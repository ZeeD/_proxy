#!/usr/bin/env python3

import http.server

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', 8080), http.server.SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
