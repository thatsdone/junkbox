#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# kafkastatus.py: A tiny kafka topic status checker
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2022/03/07 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   * kafka-pytyon-ng : As of '24/12, kafka-python 2.0 still have a problem.
#
from kafka import KafkaConsumer
from kafka import KafkaClient
from kafka.structs import TopicPartition
from kafka.structs import PartitionMetadata
from kafka.cluster import ClusterMetadata

import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kafkastatus.py')
    parser.add_argument('-t', '--topic', default='my-topic')
    parser.add_argument('-b', '--bootstrap_servers', default='localhost:9092')
    parser.add_argument('-i', '--interval', default=5)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    #
    debug = False
    if args.debug:
        debug = args.debug
    topic = args.topic
    bootstrap_servers = args.bootstrap_servers
    interval = int(args.interval)

    print('# bootstrap_servers: %s' % (bootstrap_servers))
    print('# topic: %s' % (topic))
    print('# interval: %d' % (interval))

    #
    consumer = KafkaConsumer( bootstrap_servers=bootstrap_servers)
    topics = consumer.topics()
    #
    topic_partitions = consumer.partitions_for_topic(topic)
    tps=[]
    for elm in topic_partitions:
        tp=TopicPartition(topic=topic, partition=elm)
        tps.append(tp)
    #
    consumer.assign(tps)
    #
    consumer.seek_to_beginning()
    #
    beginning_offsets = consumer.beginning_offsets(tps)
    if debug:
        print('# topic: %s'% (tp.topic))
        print('# partition ealiest_seq lastest_seq num_msgs')
        for tp in tps:
            print('  %d %d %d %d' % (tp.partition,
                                     consumer.position(tp),
                                     beginning_offsets[tp],
                                     consumer.position(tp) -
                                     beginning_offsets[tp]))

    print('# timestamp topic partitions msgs_in_topic')
    interval = 5
    while True:
        num_msgs = 0
        for tp in tps:
            num_msgs += (consumer.position(tp) - beginning_offsets[tp])

        print('%s %s %d %d' % (time.strftime("%Y/%m/%d %H:%M:%S",
                                             time.localtime()),
                               topic, len(tps), num_msgs))
        time.sleep(interval)
