#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# otetest.py: A junkbox tool for studying OpenTelemetry
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/10/14 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
import sys
import argparse
#
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

def get_traceparent(span):
    span_ctx = span.get_span_context()
    return '%s-%s-%s-%s' % (format(0, "02x"),
                            format(span_ctx.trace_id, "032x"),
                            format(span_ctx.span_id, "016x"),
                            format(span_ctx.trace_flags, "02x"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='oteltest.py')
    parser.add_argument('--service_name', default='oteltest.py')
    parser.add_argument('--otlp_exporter', default=None)
    parser.add_argument('-C', '--console', action='store_true')
    args = parser.parse_args()
    #
    resource = Resource(attributes={'service.name': sys.argv[0]})
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
    if not args.console and not args.otlp_exporter:
        print('Specify either of --console or --otlp_exporter')
        sys.exit()
    #
    # trace(1)
    #
    ctx=None
    headers11 = {}
    with tracer.start_as_current_span('span11', context=ctx) as span11:
        inject(headers11)
        span11_context = span11.get_span_context()
        print('span11 traceparent(inject): %s' % (headers11['traceparent']))
        print('span11 traceparent(manual extraction):', get_traceparent(span11))
        #
        # span12 does not use 'with' block, so end() should be called.
        # Note that the below uses start_span(), not start_as_current_span().
        #
        span12 = tracer.start_span('span12')#, context=ctx)
        headers12 = {}
        inject(headers12)
        print('span12 traceparent(inject): %s' % (headers12['traceparent']))
        print('span12 traceparent(manual extraction):', get_traceparent(span12))
        span12.end()

    #
    # trace(2)
    #
    # span21 appears outside the span11 trace tree.
    # Thus, the below is displayed as an independent trace,
    # but it's linked to span11.
    #
    span21 = tracer.start_span('span21', links=[trace.Link(span11_context)])
    headers21 = {}
    inject(headers21)
    print('span21 traceparent(inject): %s' % (headers21['traceparent'] if 'traceparent' in headers21.keys() else None))
    print('span212 traceparent(manual extraction):', get_traceparent(span21))
    span21.end()
