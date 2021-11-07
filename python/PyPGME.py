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

        # Check path element
        if not (self.path == '/metrics'):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(('<html><head><title>PyPGME</title></head>\n'
                              '<body>\n'
                              '<h1>PyPGME</h1>\n'
                              '<p><a href="/metrics"</a>Metrics<p>\n'
                              '</body></html>\n').encode('utf-8'))
            return

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
             mem_free, mem_used,
             power_draw, power_limit) = l.decode('utf-8').split(',')

            gpu_index = int(gpu_index)
            self.wfile.write(("# TYPE temperature_gpu gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP temperature.gpu of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("temperature_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_temp))).encode('utf-8'))
            self.wfile.write(("# TYPE utilization_gpu gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP utilization.gpu of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("utilization_gpu{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(gpu_util))).encode('utf-8'))
            self.wfile.write(("# TYPE utilization_memory gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP utilization.memory of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("utilization_memory{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_util))).encode('utf-8'))
            self.wfile.write(("# TYPE memory_total gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP memory.total of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("memory_total{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_total))).encode('utf-8'))
            self.wfile.write(("# TYPE memory_free gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP memory.free of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("memory_free{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_free))).encode('utf-8'))
            self.wfile.write(("# TYPE memory_used gauge\n").encode('utf-8'))
            self.wfile.write(("# HELP memory.used of nvidia-smi\n").encode('utf-8'))
            self.wfile.write(("memory_used{gpu=\"%s[%d]\"} %d\n" % (gpu_name, gpu_index, int(mem_used))).encode('utf-8'))
            if extended_attrs:
                self.wfile.write(("# TYPE pgme_power_draw gauge\n").encode('utf-8'))
                self.wfile.write(("# HELP power.draw of nvidia-smi\n").encode('utf-8'))
                self.wfile.write(("pgme_power_draw{gpu=\"%s[%d]\"} %s\n" % (gpu_name, gpu_index, power_draw)).encode('utf-8'))
                self.wfile.write(("# TYPE pgme_power_limit gauge\n").encode('utf-8'))
                self.wfile.write(("# HELP power.limit of nvidia-smi\n").encode('utf-8'))
                self.wfile.write(("pgme_power_limit{gpu=\"%s[%d]\"} %s\n" % (gpu_name, gpu_index, power_limit)).encode('utf-8'))
        return
#
#
#
if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 19101

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:b:e")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-p':
            port = int(a)
        elif o == '-b':
            bind_address = a
        elif o == '-e':
            # toggle extended_attrs
            if extended_attrs:
                extended_attrs = False
            else:
                extended_attrs = True

    httpd = HTTPServer((bind_address, port), PyPGME)

    httpd.serve_forever()
