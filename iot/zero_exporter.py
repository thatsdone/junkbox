#!/usr/bin/python3
#
# zero_exporter : A simple prometheus exporter for IoT sensors
#
# Description:
#   This is a simple prometheus exporter (initially) intended for small
#   IoT devices such as RaspberryPi Zero W. Supports multiple sensors
#   with sensor_reader.py based drivers.
#
# License:
#   Apache License, Version 2.0 (inherited from the original)
# History:
#   * 2021/06/12 v0.1 Initial version based on:
#     https://github.com/thatsdone/junkbox/blob/master/python/PyPGME.py
#   * 2021/12/08 v0.2 Add sensor reader support
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * Add HELP messages.
#
import sys
import getopt
import socket
import importlib

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

THERMAL_INPUT='/sys/class/thermal/thermal_zone0/temp'

sensors = []

class RaspiZeroExporter(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):

        self.my_hostname = socket.gethostname()
        self.my_ip = socket.gethostbyname(self.my_hostname)
        self.cpu_temp = None

        try:
            self.cpu_temp = open(THERMAL_INPUT, 'r')
        except Exception as e:
            print('Failed to open %s, skipping CPU temperator retrieval. / %s' % (THERMAL_INPUT, e))
        # import and initialize sensor driver classes
        self.driver_modules = dict()
        self.driver_classes = dict()
        # 'sensors' is a global varialbe (dict)
        for sensor in sensors:
            try:
                m = importlib.import_module(sensor['module'])
                self.driver_modules[sensor['module']] = m
                c = getattr(m, sensor['class'])
                self.driver_classes[sensor['class']] = c()
            except Exception as e:
                print('Failed to import %s. %s. Exiting...' %
                      (sensor['module'], e))
                sys.exit()

        # call super class initializer.
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
                ("raspi_zero_hwmon{raspi=\"%s\",hwmon=\"%s\",name=\"%s\"} %f\n" %
                 (self.my_hostname, "hwmon0", "cpu_thermal", (float(cpu_temp)/1000.0))).encode('utf-8'))

        # sensor is a global
        # DEBUG(thatsdone): debug code for development
        import pprint as pp
        for sensor in sensors:
            #print(sensor['class'])
            #pp.pprint(self.driver_classes[sensor['class']].get_info())
            data = self.driver_classes[sensor['class']].read_data()
            #pp.pprint(data)
            #
            for metric in data.keys():
                msg = ("raspi_zero_sensor{raspi=\"%s\",sensor=\"%s\",metric=\"%s\"} %s\n" % (self.my_hostname, sensor['class'].replace('Reader', ''), metric, data[metric])).encode('utf-8')
                #print(msg)
                self.wfile.write(msg)
        return
#
#
#
if __name__ == "__main__":

    bind_address = '0.0.0.0'
    port = 18083

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:b:s:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-p':
            port = int(a)
        elif o == '-b':
            bind_address = a
        elif o == '-s':
            for s in a.split(','):
                # 'sensor_reader.py' inherited modules expected.
                print('Configured sensor: %s' % (s))
                module = '%s_reader' % s
                class_name = '%sReader' % s.upper()
                sensors.append({'module': module,
                                'class': class_name})

    # default sensor
    if not sensors:
        sensors = [{'module':'bme680_reader', 'class':'BME680Reader'},
                   {'module':'mpu9250_reader', 'class':'MPU9250Reader'}]

    httpd = HTTPServer((bind_address, port), RaspiZeroExporter)

    httpd.serve_forever()
