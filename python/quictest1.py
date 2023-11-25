#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# quicktest1.py: A tiny test utility for testing niquests
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/11/25 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   niquests  https://niquests.readthedocs.io/en/stable/index.html
#   qh3
import argparse

import niquests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='quicktest1.py')
    parser.add_argument('--url', default=None)
    parser.add_argument('--http3', action='store_true')
    parser.add_argument('-i', '--iteration', type=int, default=1)
    parser.add_argument('-D', '--domains', nargs='*', default=None)
    args = parser.parse_args()

    # Which of HTTP/1.1, HTTP/2, HTTP/3 is used, see below:
    # https://niquests.readthedocs.io/en/stable/user/quickstart.html#http-3-over-quic
    disable_http2=False
    if args.http3:
        disable_http2=True
    session = niquests.Session(disable_http2=disable_http2)
    if args.http3:
        session.quic_cache_layer.add_domain('cloudflare-quic.com')
        session.quic_cache_layer.add_domain('www.google.com')
        # for quiche example (does not work?)
        session.quic_cache_layer.add_domain('127.0.0.1:4433')
        # Use '-D' like '-D example1.com example2.com ...'
        for domain in args.domains:
            session.quic_cache_layer.add_domain(domain)

    for i in range(0, args.iteration):
        r = session.get (args.url)
        print('iteration: ', i)
        print(r)
        print(r.status_code)
        print(r.headers)
    #print(r.text)
