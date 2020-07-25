#!/usr/bin/python3
#
# PseudoPGME : Yet another pgme running with just python3 and nvidia-smi.
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

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

command =  ['nvidia-smi',
            '--query-gpu=name,index,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used',
            '--format=csv,noheader,nounits']
#
#
#
class PseudoPGME(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        output = subprocess.Popen(command, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  close_fds=True).stdout
        self.parse_nvidia_smi(output)

    def parse_nvidia_smi(self, output):

        for line in output:
            l = line.strip()
            if len(l) < 1:
                continue

            (gpu_name, gpu_index,
             gpu_temp, gpu_util,
             mem_util, mem_total,
             mem_free, mem_used) = l.decode('utf-8').split(',')

            gpu_index = int(gpu_index)
            self.wfile.write(("temperature_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_temp))).encode('utf-8'))
            self.wfile.write(("utilization_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_util))).encode('utf-8'))
            self.wfile.write(("utilization_memory{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_util))).encode('utf-8'))
            self.wfile.write(("memory_total{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_total))).encode('utf-8'))
            self.wfile.write(("memory_free{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_free))).encode('utf-8'))
            self.wfile.write(("memory_used{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_used))).encode('utf-8'))
        return
#
#
#
if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 18080

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

    httpd = HTTPServer((bind_address, port), PseudoPGME)

    httpd.serve_forever()
