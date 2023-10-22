#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# otelmp.py: A tiny tool for reproducing OpenTelemetry multi-processing issue
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/10/21 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Note:
#   I noticed that if I used multiprocessing, OpenTelemetry spans are not
#   sent out to the collector. The behavior changes with/without '-t' option
#   (meaning threading or multiprocessing mode).
#   This is the case for both console and OTLP exporter cases at least.
import sys
import os
import argparse
import threading
import multiprocessing
#
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
#
global args

def get_traceparent(span):
    span_ctx = span.get_span_context()
    return '%s-%s-%s-%s' % (format(0, "02x"),
                            format(span_ctx.trace_id, "032x"),
                            format(span_ctx.span_id, "016x"),
                            format(span_ctx.trace_flags, "02x"))

def init_opentelemetry(service_name=None):
    print('init_opentelemetry() called. pid: %s' % (os.getpid()))
    if not service_name:
        service_name = args.service_name

    resource = Resource(attributes={'service.name': service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(args.service_name)
    if args.otlp_exporter:
        otlp_exporter = OTLPSpanExporter(endpoint=args.otlp_exporter, insecure=True)
        otlp_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(otlp_processor)
    if args.console:
        console_exporter = ConsoleSpanExporter()
        console_processor = BatchSpanProcessor(console_exporter)
        trace.get_tracer_provider().add_span_processor(console_processor)
    return tracer

def worker(tracer, idx):
    print('worker() called. idx=%d' % (idx))

    # in case of threading, initialize opentelemetry here
    service_name = 'otemp/%d' % (idx)
    if not tracer and not args.use_thread:
        tracer = init_opentelemetry(service_name=service_name)

    ctx=None
    with tracer.start_as_current_span('span11', context=ctx) as span11:
        # Note(thatsdone): don't care what I'm doing below. Anyway, some work.
        headers11 = {}
        inject(headers11)
        span11_context = span11.get_span_context()
        print('%s: span11 traceparent(inject): %s' % (service_name, headers11['traceparent']))
        print('%s: span11 traceparent(manual): %s ' % (service_name, get_traceparent(span11)))
        span11.set_status(Status(StatusCode.OK))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='otelmp.py')
    parser.add_argument('--service_name', default='otelmp.py')
    parser.add_argument('--otlp_exporter', default=None)
    parser.add_argument('-C', '--console', action='store_true')
    parser.add_argument('-n', '--num_context', type=int, default=5)
    parser.add_argument('-t', '--use_thread', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    #
    print('%s started. pid: %s' % (os.path.basename(sys.argv[0]), os.getpid()))
    if not args.console and not args.otlp_exporter:
        print('Specify either of --console or --otlp_exporter')
        sys.exit()

    if args.use_thread:
        print('threading mode.')
        tracer = init_opentelemetry()
    else:
        print('multiprocessing mode.')

    workers = []
    for idx in range(0, args.num_context):
        if args.use_thread:
            w = threading.Thread(target=worker, args=(tracer, idx,))
        else:
            w = multiprocessing.Process(target=worker, args=(None, idx))

        w.name = 'worker/%d' % (idx)
        workers.append(w)
        w.start()

    for w in workers:
        w.join()
        print('join: %s %s' % (w.name, w))

