#!/usr/bin/python3
#
# osdmon.py : Ceph OSD Monitor/Controller/Exporter
#
# Description:
#   This is a simple Ceph OSD monitor with Prometheus exporter feature.
#
#   osdmon.py does:
#   1. periodically calls 'ceph osd df -f json' (default 60s),
#   2. checks if there are osds with higher utilization than high_threshold,
#   3. set reweight value calling 'ceph osd reweight osd.OSD_ID REWEIGHT'
#      for over utilized osds
#   4. reset reweight value to 1.0 for osds with utilization lower than
#      low_threshold.
#   x. listens on 19199 (default) and returns prometheus exporter compliant
#      response for all the osds
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2025/04/15 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys, os, getopt, errno, time
import subprocess
import argparse
import json
import threading

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

global debug
global dry_run
global interval
global target_reweight
global thr_high
global thr_low

debug = False
#debug = True

#
#
#
class OSDMon(BaseHTTPRequestHandler):

    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'

        # Check path element
        if not (self.path == '/metrics'):
            msg = ('<html><head><title>OSDMon</title></head>\n'
                   '<body>\n'
                   '<h1>OSDMon</h1>\n'
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

        data = get_osd_df()
        msg = self.parse_ceph_osd_df(data)

        self.send_header('Content-Length', len(msg))
        self.end_headers()
        self.wfile.write(msg.encode('utf-8'))
        return msg

    def parse_ceph_osd_df(self, data):

        msg = ''

        osds = sorted(data['nodes'], key=lambda x: x['utilization'], reverse=True)
        for osd in osds:
            if debug:
                print("%4d %5.2f %d %d %s %s" % (osd['id'],
                                                 osd['utilization'],
                                                 osd['kb'],
                                                 osd['kb_used'],
                                                 osd['var'],
                                                 osd['status']))

            msg += "# TYPE ceph_osd_utilization gauge\n"
            msg += "# HELP ceph_osd_utilizationg\n"
            msg += "ceph_osd_utilization{osd_id=\"%s\"} %s\n" % (osd['id'],
                                                                 osd['utilization'])
            # add more metrics if necessary
        return msg
#
#
#
def get_osd_df():
    if debug:
        print('get_osd_df() called')

    buf = ''
    if not debug:
    #if not dry_run:
        command =  ['ceph', 'osd', 'df', '-f', 'json']        
        output = subprocess.Popen(command, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  close_fds=True).stdout
        for line in output:
            l = line.strip()
            if len(l) < 1 or not line:
                continue
            buf += l.decode('utf-8')
    else:
        # only for development
        with open('test-result.json') as fp:
            buf = fp.read()

    data = json.loads(buf)

    return data

def check_threshold(data, thr_high, thr_low):
    if debug:
        print('check_threshold() called')

    osds = sorted(data['nodes'], key=lambda x: x['utilization'], reverse=True)
    for osd in osds:
        #print("%4d %5.2f %d %d %s %s" % (osd['id'], osd['utilization'], osd['kb'], osd['kb_used'], osd['var'], osd['status']))
        if float(osd['utilization']) >= thr_high and osd['reweight'] == 1:
            print('Over utilized osd detected: ', osd['id'], osd['utilization'], osd['reweight'], 'setting reweight to: %s' % (target_reweight))
            set_osd_reweight(osd['id'], target_reweight)

        if float(osd['reweight']) < 1.0 and float(osd['utilization'] < thr_low):
            print('resetting reweight of osd.%d to 1.0' % (osd['id']))
            set_osd_reweight(osd['id'], 1.0)

def set_osd_reweight(osd_id, reweight):
    if debug:
        print('set_osd_reweight() called')

    buf = ''
    cmd = ['ceph', 'osd', 'reweight', 'osd.%s' % (osd_id), str(reweight)]
    if not dry_run:
        output = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  close_fds=True).stdout

        for line in output:
           l = line.strip()
           if len(l) < 1 or not line:
               continue
           buf += l.decode('utf-8')

        print(time.time(),  ': ceph osd reweight osd.%s %s result: ' % (osd_id), str(reweight))
        print(buf)

    else:
        print('set_osd_reweight(): dry_run mode: ', cmd)


def monitor_thread(cv, thr_high, thr_low):
    if debug:
        print('monitor_thread: started', cv, thr_high, thr_low)
    last_log = time.time()
    print('%s: monitor_thread(): calling get_osd_df() (hourly report)' %(last_log))
    while True:
        if debug:
            print('ts: ', time.time())
        now = time.time()
        if now - last_log > 3600:
            print('%s: monitor_thread(): calling get_osd_df() (hourly report)' %(now))
            last_log = now
        data = get_osd_df()
        check_threshold(data, thr_high, thr_low)
        time.sleep(interval)
#
#
#
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='osdmon.py')
    parser.add_argument('-b', '--bind_address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=19199)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('-i', '--interval', type=int, default=60)
    parser.add_argument('-t', '--high_threshold', type=float, default=94.0)
    parser.add_argument('-l', '--low_threshold', type=float, default=93.0)
    parser.add_argument('-r', '--target_reweight', type=float, default=0.8)
    args = parser.parse_args()

    debug = args.debug
    dry_run = args.dry_run
    target_reweight = args.target_reweight
    thr_high =args.high_threshold 
    thr_low = args.low_threshold 

    bind_address = args.bind_address
    port = args.port

    httpd = HTTPServer((bind_address, port), OSDMon)

    interval = 60
    cv = threading.Condition()
    th1 = threading.Thread(target=monitor_thread,
                           args=(cv,
                                 args.high_threshold,
                                 args.low_threshold))
    th1.start()

    httpd.serve_forever()
