#!/usr/bin/env python

import urllib.request
import operator

RESOURCE = 'http://skygo.sky.it/config/config.min.js'

def proxy():
    opener = urllib.request.ProxyHandler({ 'http': 'http://localhost:9999' })
    urllib.request.install_opener(urllib.request.build_opener(opener))
    return urllib.request.urlopen(RESOURCE)

def get():
    return urllib.request.urlopen(RESOURCE)

def test():
    response_get = get()
    response_proxy = proxy()

    for attr in ( 'msg', 'status', 'reason' ):
        f = operator.attrgetter(attr)
        assert f(response_get) == f(response_proxy), attr

    headers_get = response_get.getheaders()
    headers_proxy = response_proxy.getheaders()

    for ((header_get, value_get), (header_proxy, value_proxy)) in zip(headers_get, headers_proxy):
        assert header_get == header_proxy, 'header %r - %r' % (header_get, header_proxy)
        if header_get not in ('Date', 'Expires'):
            assert value_get == value_proxy, 'value %r - %r' % (value_get, value_proxy)

    body_get = response_get.read()
    body_proxy = response_proxy.read()

    assert body_get == body_proxy, 'body %r - %r' % (body_get, body_proxy)


def loop(n=100):
    for _ in range(n):
        test()

if __name__ == '__main__':
    loop()