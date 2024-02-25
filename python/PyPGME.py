#!/usr/bin/python3
#
# PyPGME : Yet another pgme running with just python3 and nvidia-smi.
#
# Description:
#   This script returns compatible response with PGME
#   (Prometheus GPU Metrics Exporter) available at:
#     https://github.com/chhibber/pgme
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2020/07/24 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys, os, getopt, errno
import subprocess
import argparse

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

command =  ['nvidia-smi',
            '--query-gpu=name,index,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,power.draw,power.limit',
            '--format=csv,noheader,nounits']
extended_attrs = True
#
#
#
class PyPGME(BaseHTTPRequestHandler):

    def do_GET(self):
        # FIXME(thatsdone): Are there appropriate initializers?
        self.protocol_version = 'HTTP/1.1'

        # Check path element
        if not (self.path == '/metrics'):
            msg = ('<html><head><title>PyPGME</title></head>\n'
                   '<body>\n'
                   '<h1>PyPGME</h1>\n'
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
        #self.end_headers()

        output = subprocess.Popen(command, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  close_fds=True).stdout
        msg = self.parse_nvidia_smi(output)
        self.send_header('Content-Length', len(msg))
        self.end_headers()
        self.wfile.write(msg.encode('utf-8'))
        return

    def parse_nvidia_smi(self, output):

        msg = ''

        for line in output:
            l = line.strip()
            if len(l) < 1:
                continue

            (gpu_name, gpu_index,
             gpu_temp, gpu_util,
             mem_util, mem_total,
             mem_free, mem_used,
             power_draw, power_limit) = l.decode('utf-8').split(',')

            gpu_index = int(gpu_index)
            msg += "# TYPE temperature_gpu gauge\n"
            msg += "# HELP temperature.gpu of nvidia-smi\n"
            msg += "temperature_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_temp))
            msg += "# TYPE utilization_gpu gauge\n"
            msg += "# HELP utilization.gpu of nvidia-smi\n"
            msg += "utilization_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_util))
            msg += "# TYPE utilization_memory gauge\n"
            msg += "# HELP utilization.memory of nvidia-smi\n"
            msg += "utilization_memory{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_util))
            msg += "# TYPE memory_total gauge\n"
            msg += "# HELP memory.total of nvidia-smi\n"
            msg += "memory_total{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_total))
            msg += "# TYPE memory_free gauge\n"
            msg += "# HELP memory.free of nvidia-smi\n"
            msg += "memory_free{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_free))
            msg += "# TYPE memory_used gauge\n"
            msg += "# HELP memory.used of nvidia-smi\n"
            msg += "memory_used{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_used))
            if extended_attrs:
                msg += "# TYPE pgme_power_draw gauge\n"
                msg += "# HELP power.draw of nvidia-smi\n"
                msg += "pgme_power_draw{gpu=\"%s[%d]\"} %s\n" % (gpu_name, gpu_index, power_draw)
                msg += "# TYPE pgme_power_limit gauge\n"
                msg += "# HELP power.limit of nvidia-smi\n"
                msg += "pgme_power_limit{gpu=\"%s[%d]\"} %s\n" % (gpu_name, gpu_index, power_limit)
        return msg
#
#
#
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyPGME.py')
    parser.add_argument('-b', '--bind_address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=19101)
    parser.add_argument('-e', '--extended_attribute', action='store_true')
    args = parser.parse_args()
    
    bind_address = args.bind_address
    port = args.port
    extended_attrs = args.extended_attribute

    httpd = HTTPServer((bind_address, port), PyPGME)

    httpd.serve_forever()
