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
# TODO:
#   * DONE: handle GET /v3/auth/tokens
#   * rewrite endpoints (append given endpoint information)
#   * handle GET /v3/endpoints
#   * handle GET /v3/services
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

    def pass_through(self, method):
        global args
        # Just pass through the received request.
        # NOTE(thatsdone): OpenStack Keystone does not use PUT.
        r = None
        if method == 'GET':
            r = requests.get(args.os_auth_url,
                             headers=self.headers,
                             timeout=args.timeout)
        if method == 'HEAD':
            r = requests.head(args.os_auth_url,
                              headers=self.headers,
                              timeout=args.timeout)
        if method == 'DELETE':
            r = requests.get(args.os_auth_url,
                             headers=self.headers,
                             timeout=args.timeout)
        if method == 'POST':
            if 'Content-Length' in self.headers:
                content_length = int(self.headers['Content-Length'])
            else:
                content_length = 0
            post_data = self.rfile.read(content_length)
            r = requests.post(args.os_auth_url,
                              headers=self.headers,
                              timeout=args.timeout,
                              data=post_data)

        if args.debug:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        #
        self.protocol_version = 'HTTP/1.1'
        self.send_response(r.status_code)
        for key in r.headers.keys():
            self.send_header(key, r.headers[key])
        self.end_headers()
        self.wfile.write(r.text.encode('utf-8'))
        return

    def do_HEAD(self):
        self.pass_through('HEAD')

    def do_DELETE(self):
        self.pass_through('DELETE')

    def do_GET(self):
        self.pass_through('GET')

    def do_POST(self):
        global args

        if not self.path == '/v3/auth/tokens':
            self.pass_through('POST')

        else:
            if args.debug:
                print('do_POST() called: %s' % (self.path))

            if 'Content-Length' in self.headers:
                content_length = int(self.headers['Content-Length'])
            else:
                content_length = 0
            post_data = self.rfile.read(content_length)
            #
            url = args.os_auth_url + '/auth/tokens'
            r = requests.post(url,
                              headers=self.headers,
                              timeout=args.timeout,
                              data=post_data)
            if args.debug:
                print(r.status_code)
                print(type(r.headers))
                print(r.headers)
            self.protocol_version = 'HTTP/1.1'
            self.send_response(r.status_code)
            #self.send_response(HTTPStatus.OK)
            for key in r.headers.keys():
                self.send_header(key, r.headers[key])
                if args.debug:
                    print(key, r.headers[key])
            self.end_headers()
            if args.append_endpoints:
                print(r.text)
                result = json.loads(r.text)
                for elm in result['token']['catalog']:
                    print(elm['name'], elm['id'])
                    for ep in elm['endpoints']:
                        print('    ', ep['id'], ep['interface'],
                              ep['region_id'], ep['region'], ep['url'])
            self.wfile.write(r.text.encode('utf-8'))


if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 19102

    parser = argparse.ArgumentParser(description='KeystoneProxy.py')
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument('-0', '--bind', default='0.0.0.0')
    parser.add_argument('--os_auth_url', default=None)
    parser.add_argument('--timeout', type=int, default=10)
    parser.add_argument('--append_endpoints', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    port = args.port
    bind_address = args.bind

    if not args.os_auth_url:
        print('Specify the target Keystone endpoint via --os_auth_url')
        sys.exit()

    print('Starting KeystoneProxy.py listening at %s:%d'
          % (args.bind, args.port))

    httpd = HTTPServer((bind_address, port), KeyStoneProxy)
    if args.append_endpoints:
        print('Loading...: %s' % (args.append_endpoints))
        with open(args.append_endpoints) as fd:
            httpd.conf = yaml.load(fd, Loader=yaml.SafeLoader)
        if args.debug:
            print(httpd.conf)

    httpd.serve_forever()
