#!/usr/bin/python3
#
# zero_exporter : A simple prometheus exporter for RaspberryPi Zero W
#
# Description:
#   This script returns just CPU temperature (at the moment).
#
# License:
#   Apache License, Version 2.0 (inherited from the original)
# History:
#   * 2021/06/12 v0.1 Initial version based on:
#     https://github.com/thatsdone/junkbox/blob/master/python/PyPGME.py
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys
import os
import getopt
import errno
import socket
import time
import datetime

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

import smbus
import struct

THERMAL_INPUT='/sys/class/thermal/thermal_zone0/temp'


class RaspiZeroExporter(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.my_hostname = socket.gethostname()
        self.my_ip = socket.gethostbyname(self.my_hostname)
        #print("DEBUG: debug: __init__() %s %s %s" % (arg1, arg2, arg3))
        try:
            self.cpu_temp = open(THERMAL_INPUT, 'r')
        except Exception:
            self.cpu_temp = None
            print('%s does not exist. Skipping CPU temp. poll' % (THERMAL_INPUT))
        super().__init__(request, client_address, server)
        return

    def do_GET(self):
        if not (self.path == '/metrics'):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(('<html><head><title>zero_exporter</title></head>\n'
                              '<body>\n'
                              '<h1>zero_exporter</h1>\n'
                              '<p><a href="/metrics"</a>Metrics<p>\n'
                              '</body></html>\n').encode('utf-8'))
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        if self.cpu_temp:
            cpu_temp = self.cpu_temp.read()
            self.wfile.write(
                ("raspi_hwmon{raspi=\"%s\",hwmon=\"%s\",name=\"%s\"} %f\n" %
                 (self.my_hostname, "hwmon0", "cpu_thermal", (float(cpu_temp)/1000.0))).encode('utf-8'))
        return
#
#
#
if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 18083

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:b:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-p':
            port = int(a)
        elif o == '-b':
            bind_address = a

    httpd = HTTPServer((bind_address, port), RaspiZeroExporter)

    httpd.serve_forever()
