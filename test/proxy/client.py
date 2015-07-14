#!/usr/bin/env python

import urllib.request

def proxy():
    # GET http://localhost:8080/server.py HTTP/1.1\r\n
    # Accept-Encoding: identity\r\n
    # Host: localhost:8080\r\n
    # Connection: close\r\n
    # User-Agent: Python-urllib/3.4\r\n
    # \r\n

    opener = urllib.request.ProxyHandler({
        'http': 'http://localhost:9999'
    })
    urllib.request.install_opener(urllib.request.build_opener(opener))

    return urllib.request.urlopen('http://skygo.sky.it/config/config.min.js')

def get():
    # GET / HTTP/1.1\r\n
    # Accept-Encoding: identity\r\n
    # Host: localhost:9999\r\n
    # Connection: close\r\n
    # User-Agent: Python-urllib/3.4\r\n
    # \r\n

    return urllib.request.urlopen('http://localhost:9999')

if __name__ == '__main__':
    response = proxy()
    print('msg: %r' % (response.msg))
    print('status: %r' % (response.status))
    print('reason: %r' % (response.reason))

    print('headers:')
    for (header, value) in  response.getheaders():
        print('\t%r: %r' % (header, value))

    print('--------------------\nbody: \n%r' % (response.read()))
