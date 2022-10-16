#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# kafkaheader.py: A sample program to access Kafka Headers from python
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
from kafka import KafkaProducer
from kafka import KafkaConsumer

topic = 'KAFKA_TOPIC'
bootstrap_servers = 'KAFKA_BOOTSTRAP:9092'

max_request_size=1024*1024


if len(sys.argv) < 2:
    print("Specify 'send' or 'recv'")
    sys.exit()

if sys.argv[1] == 'send':
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    raw_bytes=bytes('payload_data', 'utf-8')
    #print(type(raw_bytes), raw_bytes)
    value1 =  bytes('value1', 'utf-8')
    value2 =  bytes('value2', 'utf-8')
    future = producer.send(topic, value=raw_bytes , headers=[('key1', value1), ('key2', value2)])
    result = future.get(timeout=10)
    print(result)

elif sys.argv[1] == 'recv':
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(topics=[topic])
    while True:
        result = consumer.poll(timeout_ms=3600*1000, max_records=1024)
        for k in result:
            print('RESULT KEY: ', k, type(result[k]), result[k])
            for elm in result[k]:
                print('ELM: ', type(elm), 'topic: ', elm.topic, 'partition: ', elm.partition, 'value: ', elm.value)
                for  h in elm.headers:
                    print(h, type(h), h[0], h[1])
else:
    print('Unkown argument: ', sys.argv[1])
