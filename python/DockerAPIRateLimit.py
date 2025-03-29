#!/usr/bin/python3
#
# DockerAPIRateLimit.py
#
# Description:
#  This is a simple Prometheus Exporter to return docker API rate limit status
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2025/03/15 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
# References:
#   * https://docs.docker.com/docker-hub/usage/pulls/#view-hourly-pull-rate-and-limit
#
import sys, os, getopt, errno
import argparse
import requests
import json

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus
#
#
#
class DockerAPIRateLimit(BaseHTTPRequestHandler):

    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        # Check path element
        if not (self.path == '/metrics'):
            msg = ('<html><head><title>DockerAPIRateLimit</title></head>\n'
                   '<body>\n'
                   '<h1>DockerAPIRateLimit</h1>\n'
                   '<p><a href="/metrics"</a>Metrics<p>\n'
                   '</body></html>\n')
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(msg))
            self.end_headers()
            self.wfile.write(msg.encode('utf-8'))
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/plain')


        (status_code, ratelimit, remaining, source) = get_rate_limit()

        msg = ''
        if status_code == HTTPStatus.OK:
            msg += "# TYPE docker_api_ratelimit_limit gauge\n"
            msg += "# HELP docker_api_ratelimit_limit\n"
            msg += "docker_api_ratelimit_limit{source=\"%s\"} %d\n" % (source, int(ratelimit.split(';')[0]))
            msg += "# TYPE docker_api_ratelimit_remaining gauge\n"
            msg += "# HELP docker_api_ratelimit_remaining\n"
            msg += "docker_api_ratelimit_remaining{source=\"%s\"} %d\n" % (source, int(remaining.split(';')[0]))

        self.send_header('Content-Length', len(msg))
        self.end_headers()
        self.wfile.write(msg.encode('utf-8'))
        return

def get_rate_limit():

    # get a token
    token_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull'
    r = requests.get(token_url)
    rr = json.loads(r.text)
    # query rate limit status
    headers = {}
    headers['Authorization'] = "Bearer %s" % (rr['token'])
    rate_url = 'https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest'
    rrr = requests.get(rate_url, headers=headers)
    if rrr.status_code == 200:
        return rrr.status_code, rrr.headers['ratelimit-limit'], rrr.headers['ratelimit-remaining'], rrr.headers['docker-ratelimit-source']
    else:
        return rrr.status_code, None, None, None
#
#
#
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='DockerAPIRateLimit.py')
    parser.add_argument('-b', '--bind_address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=29290)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    bind_address = args.bind_address
    port = args.port

    httpd = HTTPServer((bind_address, port), DockerAPIRateLimit)

    httpd.serve_forever()
