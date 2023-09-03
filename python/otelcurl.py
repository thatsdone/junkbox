#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# otelcurl.py: A tiny utility for testing OpenTelemetry/HTTP test
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/09/01 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   See below imports (opentelemetry)
import sys
import time
import datetime
import argparse
import requests

from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='otelcurl.py')
    parser.add_argument('--url', default=None)
    parser.add_argument('-X', '--method', default='GET',
                        help='Currently supported methods: GET, POST')
    parser.add_argument('--data_raw', default=None,
                        help='If you start the DATA_RAW with the letter @, the rest  should  be  a filename like curl.')
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--endpoint', default=None,
                        help='OTLP Collector Endpoint (e.g. http://localhost:4317)')
    parser.add_argument('--console', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--forward_url', default=None)
    args = parser.parse_args()
    #
    # Setup OpenTelemetry
    #
    resource = Resource(attributes={'service.name': sys.argv[0]})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(sys.argv[0])
    if args.endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=args.endpoint, insecure=True)
        otlp_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(otlp_processor)
    if args.console:
        console_exporter = ConsoleSpanExporter()
        console_processor = BatchSpanProcessor(console_exporter)
        trace.get_tracer_provider().add_span_processor(console_processor)

    #
    # Generate an HTTP request
    #
    headers = {}
    with tracer.start_as_current_span("%s" % (sys.argv[0])) as span:
        inject(headers)
        if args.debug:
            print(headers)
        if args.method == 'GET':
            r = requests.get(args.url,
                         headers=headers,
                         timeout=args.timeout)
            print(r.status_code)
            #print(r.text)
        elif args.method == 'POST':
            if args.data_raw and args.data_raw[0] == '@':
                with open(args.data_raw[1:], 'rb') as fp:
                    raw_bytes = fp.read()
            else:
                raw_bytes = bytes(args.data_raw, 'utf-8')
            headers['Content-Length'] = str(len(raw_bytes))
            if args.forward_url:
                headers['forward_url'] = args.forward_url
            r = requests.post(args.url,
                              headers=headers,
                              timeout=args.timeout,
                              data=raw_bytes)
            print(r.status_code)
        elif args.method:
            print('method: %s not supported.'  % (args.method))
