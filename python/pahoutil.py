#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pahoutil.py: A simple Eclipse Paho Python util to show how it works.
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/10/01 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   * paho-mqtt: https://pypi.org/project/paho-mqtt/
# Note:
#   * Regarding QoS 2, see below as of now.
#     * https://github.com/eclipse/paho.mqtt.python/issues/696
#
import sys
import argparse
# common
import paho.mqtt.client as mqtt
# for client
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
#
#
#
def on_log(mqttc, userdata, level, string):
    print('on_log(): %s : %s %s' % (userdata, level, string))

def on_connect(client, userdata, flags, rc, props):
    print('on_connect(): %s : %s %s %s' % (userdata, flags, rc, props))

def on_disconnect(client, userdata, rc, foo):
    print('on_disconnect(): %s : %s %s' % (userdata, rc, foo))

def on_publish(mqttc, userdata, mid):
    print('on_publish(): %s : %s' % (userdata, mid))

def on_subscribe(mqttc, userdata, mid, rc, granted_qos):
    print('on_subscribe(): %s : %s %s' % (userdata, rc, granted_qos))

def on_message(client, userdata, msg):
    print('on_message(): %s : %s %s %s %s / %s' % (userdata, msg.topic,
                                                   msg.mid, msg.timestamp,
                                                   msg.retain,
                                                   msg.payload.decode()))

def message(client, userdata, msg):
    print('message(): %s : %s %s %s %s / %s' % (userdata, msg.topic,
                                                msg.mid, msg.timestamp,
                                                msg.retain,
                                                msg.payload.decode()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pahoutil.py')
    parser.add_argument('-o', '--operation', default='server')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--mqtt_version', type=int, default=5)
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', type=int, default=1883)
    parser.add_argument('--topic', default='topic1')
    parser.add_argument('--qos', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--message', default='Hello, world!')
    parser.add_argument('--interval', type=int, default=10)
    parser.add_argument('--tls', action='store_true')
    parser.add_argument('--cacert', default=None)
    parser.add_argument('--cert', default=None)
    parser.add_argument('--key', default=None)
    parser.add_argument('--tls_secure', action='store_true')
    args = parser.parse_args()

    print(f'Using... host: {args.host} port: {args.port} mqtt version: {args.mqtt_version} topic: {args.topic} qos: {args.qos}')

    if not args.host:
        print('Specify at least --host')
        sys.exit()

    if args.operation == 'server':
        userdata = 'server'
        mqttc = mqtt.Client(protocol=mqtt.MQTTv5, userdata=userdata)
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_disconnect = on_disconnect
        mqttc.on_publish = on_publish
        mqttc.on_subscribe = on_subscribe
        mqttc.on_log = on_log

        if args.tls:
            if not args.cacert:
                print('Specify --cacert')
                sys.exit()
            mqttc.tls_set(ca_certs=args.cacert,
                          certfile=args.cert, keyfile=args.key)
            if not args.tls_secure:
                mqttc.tls_insecure_set(True)

        mqttc.connect(args.host, args.port, args.timeout)
        mqttc.message_callback_add(args.topic, message)

        mqttc.subscribe(args.topic, args.qos)

        mqttc.loop_forever()

    elif args.operation == 'client':

        client_id = 'client'
        mqttc = mqtt.Client(client_id=client_id,
                            protocol=mqtt.MQTTv5, userdata='client')
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_disconnect = on_disconnect
        mqttc.on_publish = on_publish
        mqttc.on_subscribe = on_subscribe
        mqttc.on_log = on_log

        if args.tls:
            if not args.cacert:
                print('Specify --cacert')
                sys.exit()
            mqttc.tls_set(ca_certs=args.cacert,
                          certfile=args.cert, keyfile=args.key)
            if not args.tls_secure:
                mqttc.tls_insecure_set(True)

        properties=Properties(PacketTypes.CONNECT)
        properties.SessionExpiryInterval=args.interval
        mqttc.connect(host=args.host,
                      port=args.port,
                      keepalive=args.interval,
                      clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY
                      #,properties=properties
                      )

        mqttc.message_callback_add(args.topic, message)

        print('publish(): publishing a message to: %s payload: %s' % (args.topic, args.message))

        prop2=Properties(PacketTypes.PUBLISH)
        prop2.MessageExpiryInterval=10
        prop2.UserProperty = ('traceparent', '00-dummy-traceparent-01')

        mqttc.publish(args.topic, args.message.encode('utf-8'),
                      qos=args.qos, properties=prop2)
        mqttc.disconnect()

        #mqttc.loop_forever()

    else:
        print('Invalid operation %s' % (args.operation))
