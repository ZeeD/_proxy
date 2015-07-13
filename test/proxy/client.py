#!/usr/bin/env python

import urllib.request

if __name__ == '__main__':
    opener = urllib.request.ProxyHandler({
        'http': 'http://localhost:9999'
    })
    urllib.request.install_opener(urllib.request.build_opener(opener))
    response = urllib.request.urlopen('http://localhost:8080/server.py')
    print('msg: %r' % (response.msg))
    print('status: %r' % (response.status))
    print('reason: %r' % (response.reason))

    print('headers:')
    for (header, value) in  response.getheaders():
        print('\t%r: %r' % (header, value))

    print('--------------------\nbody: \n%r' % (response.read()))
