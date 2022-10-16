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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kafkacli.py')
    parser.add_argument('-t', '--topic', default='my-topic')
    parser.add_argument('-b', '--bootstrap_servers', default='localhost:9092')
    parser.add_argument('-p', '--poll_timeout', type=int, default=5)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-R', '--recv', action='store_true', default=False)
    parser.add_argument('-S', '--send', action='store_true', default=False)
    parser.add_argument('-m', '--message', default=None)
    args = parser.parse_args()
    #
    debug = False
    if args.debug:
        debug = args.debug
    topic = args.topic
    bootstrap_servers = args.bootstrap_servers
    interval = args.poll_timeout

    if args.recv and args.send:
        print('-R(--recv) and -S(--send) are exclusive')
        sys.exit()
    elif not (args.recv and args.send):
        print('Running receiver mode (-R)')
        args.recv = True

    print('# kafkacli.py : Running %s mode' % ('receiver' if args.recv else 'sender'))
    print('# bootstrap_servers: %s' % (bootstrap_servers))
    print('# topic: %s' % (topic))
    print('# poll timeout: %d (s)' % (args.poll_timeout))

    if args.send:
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        if args.message:
            raw_bytes=bytes(args.message, 'utf-8')
        else:
            raw_bytes=bytes('payload_data', 'utf-8')
        #print(type(raw_bytes), raw_bytes)
        value1 =  bytes('value1', 'utf-8')
        value2 =  bytes('value2', 'utf-8')
        future = producer.send(topic, value=raw_bytes , headers=[('key1', value1), ('key2', value2)])
        result = future.get(timeout=10)
        print(result)

    elif args.recv:
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        consumer.subscribe(topics=[topic])
        while True:
            result = consumer.poll(timeout_ms=args.poll_timeout*1000, max_records=1024)
            for k in result:
                print('RESULT KEY: ', k, type(result[k]), result[k])
                for elm in result[k]:
                    print('ELM: ', type(elm), 'topic: ', elm.topic, 'partition: ', elm.partition)
                    print('payload: %s' % (elm.value.decode()))
                    for  h in elm.headers:
                        #print('headers: %s %s 'h, type(h))
                        print('headers: %s = %s' % (h[0], h[1].decode()))
