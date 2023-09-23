#!/usr/bin/python3
#
# KeystoneProxy : An OpenStack Keystone proxy allowing response rewite
#
# Description:
#   Works as a proxy server with some response rewriting functions.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2023/09/23 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys
import argparse
import requests
import json
import yaml
#
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus
#
#
#
class KeyStoneProxy(BaseHTTPRequestHandler):

    def do_GET(self):
        global args
        self.protocol_version = 'HTTP/1.1'
        msg = ''
        self.send_response(HTTPStatus.OK)
        if self.path == '/v3':
            r = requests.get(args.os_auth_url,
                             headers=self.headers,
                             timeout=10)
            if args.debug:
                print(r.status_code)
                print(r.headers)
                print(r.text)
            #
            for key in r.headers.keys():
                self.send_header(key, r.headers[key])
            self.end_headers()
            msg = r.text
        self.wfile.write(msg.encode('utf-8'))
        return

    def do_POST(self):
        global args
        print('do_POST() called: %s' % (self.path))
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
        else:
            content_length = 0
        headers = {}
        post_data = self.rfile.read(content_length)
        self.protocol_version = 'HTTP/1.1'
        self.send_response(HTTPStatus.OK)
        #
        if self.path == '/v3/auth/tokens':
            url = args.os_auth_url + '/auth/tokens'
            r = requests.post(url,
                              headers=headers,
                              timeout=10,
                              data=post_data)
            if args.debug:
                print(r.status_code)
                print(type(r.headers))
                print(r.headers)
            for key in r.headers.keys():
                if args.debug:
                    print(key, r.headers[key])
                self.send_header(key, r.headers[key])
            self.end_headers()
            if args.debug:
                print(r.text)
                result = json.loads(r.text)
                for elm in result['token']['catalog']:
                    print(elm['name'], elm['id'])
                    for ep in elm['endpoints']:
                        print('    ', ep['id'], ep['interface'],
                              ep['region_id'], ep['region'], ep['url'])
            msg = r.text
            self.send_response(r.status_code)
            self.wfile.write(msg.encode('utf-8'))
#
#
#
if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 19102

    parser = argparse.ArgumentParser(description='KeystoneProxy.py')
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument('-0', '--bind', default='0.0.0.0')
    parser.add_argument('--os_auth_url', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    port = args.port
    bind_address = args.bind

    httpd = HTTPServer((bind_address, port), KeyStoneProxy)

    httpd.serve_forever()
