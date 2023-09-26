#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# kafkacli.py: A simple kafka consumer/producer sample including Kafka Headers
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2022/06/26 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   * kafka-pytyon : https://kafka-python.readthedocs.io/
#
import sys
import argparse
from kafka import KafkaProducer
from kafka import KafkaConsumer

topic = 'my-topic'
bootstrap_servers = '127.0.0.1:9092'

#max_request_size=1024*1024

def get_traceparent(span):
    span_ctx = span.get_span_context()
    return '%s-%s-%s-%s' % (format(0, "02x"),
                            format(span_ctx.trace_id, "032x"),
                            format(span_ctx.span_id, "016x"),
                            format(span_ctx.trace_flags, "02x"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kafkacli.py')
    parser.add_argument('-t', '--topic', default='my-topic')
    parser.add_argument('-b', '--bootstrap_servers', default='localhost:9092')
    parser.add_argument('-p', '--poll_timeout', type=int, default=5)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-R', '--recv', action='store_true', default=False)
    parser.add_argument('-S', '--send', action='store_true', default=False)
    parser.add_argument('-m', '--message', default=None)
    parser.add_argument('--dump_size', type=int, default=256)
    parser.add_argument('--enable_otel', action='store_true')
    parser.add_argument('--endpoint', default=None)
    parser.add_argument('--console', action='store_true')
    args = parser.parse_args()
    #
    debug = False
    if args.debug:
        debug = args.debug
    topic = args.topic
    bootstrap_servers = args.bootstrap_servers
    interval = args.poll_timeout

    tracer = None
    if args.enable_otel:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.propagate import inject
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
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

    if args.recv and args.send:
        print('-R(--recv) and -S(--send) are exclusive')
        sys.exit()
    elif (args.recv == False and args.send == False):
        args.recv = True

    print('# kafkacli.py : Running %s mode' % ('receiver(-R)' if args.recv else 'sender(-S)'))
    print('# bootstrap_servers: %s' % (bootstrap_servers))
    print('# topic: %s' % (topic))
    print('# poll timeout: %d (s)' % (args.poll_timeout))

    if args.send:
        traceparent = 'dummy_otel_not_enabled'
        if args.enable_otel:
            #with tracer.start_as_current_span("ProducerRecord") as span1:
            span1 = tracer.start_span("ProducerRecord", context=None)
            traceparent = get_traceparent(span1)
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        if args.message:
            raw_bytes=bytes(args.message, 'utf-8')
        else:
            raw_bytes=bytes('payload_data', 'utf-8')
        future = producer.send(topic, value=raw_bytes,
                               headers=[('traceparent', bytes(traceparent, 'utf-8'))])
        result = future.get(timeout=10)
        print(result)

        if args.enable_otel:
            span1.end()

    elif args.recv:
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        consumer.subscribe(topics=[topic])
        while True:
            result = consumer.poll(timeout_ms=args.poll_timeout*1000, max_records=1024)
            for k in result:
                print('RESULT KEY: ', k, type(result[k]), result[k])
                for elm in result[k]:
                    print('ELM: ', type(elm), 'topic: ', elm.topic, 'partition: ', elm.partition)
                    #
                    traceparent = None
                    for  h in elm.headers:
                        #print('headers: %s %s 'h, type(h))
                        print('headers: %s = %s' % (h[0], h[1].decode()))
                        if not traceparent and h[0] == 'traceparent':
                            traceparent = h[1].decode()

                    if args.enable_otel:
                        ctx = None
                        if traceparent:
                            carrier = {'traceparent': traceparent}
                            ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
                        span1 = tracer.start_span("ConsumerRecord", context=ctx)
                    #
                    #print('payload: %s' % (elm.value.decode()))
                    post_data = elm.value
                    print('payload:')
                    if len(post_data) > args.dump_size:
                        dump_size = args.dump_size
                    else:
                        dump_size = len(post_data)
                    dump_str = ''
                    for i in range(0, dump_size):
                        dump_str += '%02x ' % (post_data[i])
                        if ((i + 1) % 16) == 0:
                            print(dump_str)
                            dump_str = ''
                    if (dump_size % 16 != 0):
                        print(dump_str)
                    if args.enable_otel:
                        span1.end()
