#!/usr/bin/python3
#
# pub1.py : An example to use AWS IoT Core Python SDK
#
# Description:
#  * publishes an MQTT message to the sepcified topic.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/30 v0.1 Initial version based on:
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * Add HELP messages.
#
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import threading

import time
import getopt
import sys
import uuid

import yaml

def handler_conn_interrupted(connection, errno, **kwargs):
    print('handler_conn_interrupt: ')
    return

def handler_conn_resumed(connection, return_code, session_present, **kwargs):
    print('handler_conn_resume: ')
    resubscribe_future.add_done_callback(handler_resubscribe_complete)
    return

# registered by in on_connection_resumed handler.
def handler_resubscribe_complete(resubscribe_future):
    print('handler_resubscribe_complete: ')
    return

def usage():
    print('USAGE: %s:' % (sys.argv[0]))

# registered by mqtt_connection.subscribe() on subscribe time in main.
def handler_message_received(topic, payload, dup, qos, retain, **kwargs):
    print('handler_message_received: ')


if __name__ == '__main__':

    conf_file = 'pub1.yaml'

    endpoint = None
    thing = None
    root_ca = None
    cert = None
    key = None
    cred_dir = None
    topic = None
    ca_certificate = None
    msg = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:c:k:t:f:m:h")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-f':
            conf_file = a
        elif o == '-e':
            endpoint = a
        elif o == '-c':
            ca_certificate = a
        elif o == '-k':
            key = a
        elif o == '-t':
            topic = a
        elif o == '-m':
            msg = a
        elif o == '-h':
            usage()
            sys.exit()

    conf=None
    if conf_file:
        try:
            with open(conf_file, 'r') as ymlconf:
                conf=yaml.load(ymlconf, Loader=yaml.SafeLoader)
                if not cred_dir and conf['creds']['cred_dir']:
                    cred_dir = conf['creds']['cred_dir']
                if not root_ca and conf['creds']['root_ca']:
                    root_ca = conf['creds']['root_ca']
                if not endpoint and conf['creds']['endpoint']:
                    endpoint = conf['creds']['endpoint']
                if not key and conf['creds']['private_key']:
                    key = conf['creds']['private_key']
                if not ca_certificate and conf['creds']['ca_certificate']:
                    ca_certificate = conf['creds']['ca_certificate']
                if not topic and conf['creds']['topic']:
                    topic = conf['creds']['topic']
                if not thing and conf['creds']['thing']:
                    thing = conf['creds']['thing']
        except Exception as e:
            print('%s does not exist. %s' % (conf_file, e))
            sys.exit()

    if not endpoint:
        print('endpoint is null')
        sys.exit()
    if not root_ca:
        print('ca_certificate is null')
        sys.exit()
    if not key:
        print('key is null')
        sys.exit()
    if not topic:
        print('topic is null')
        sys.exit()
    if not ca_certificate:
        print('endpoint is null')
        sys.exit()

    print('Sending a message to topic: %s' % (topic))

#    print(
#    endpoint,
#    thing,
#    root_ca,
#    key,
#    cred_dir,
#    topic,
#    ca_certificate)

    received_all_event = threading.Event()
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    keep_alive_secs = 6

    if thing:
        client_id = '%s-%s' %  (thing, uuid.uuid4())
        ca_filepath='%s/%s' % (cred_dir, root_ca)
        cert_filepath='%s/%s-certificate.pem.crt' % (cred_dir, thing)
        pri_key_filepath='%s/%s-private.pem.key' % (cred_dir, thing)
    else:
        client_id = '%s-%s' %  ('temp', uuid.uuid4())
        ca_filepath='%s/%s' % (cred_dir, root_ca)
        cert_filepath='%s/%s' % (cred_dir, ca_certificate)
        pri_key_filepath='%s/%s' % (cred_dir, key)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert_filepath,  # certificate.pem.crt
        pri_key_filepath=pri_key_filepath,  # private.pem.key
        ca_filepath=ca_filepath,  # root_ca
        on_connection_interrupted=handler_conn_interrupted,
        on_connection_resumed=handler_conn_resumed,
        client_id=client_id,
        cleans_session=False,
        keep_alive_secs=keep_alive_secs,
        client_bootstrap=client_bootstrap
    )

    print('Connecting to %s with client ID %s' % (endpoint, client_id))
    connect_future = mqtt_connection.connect()
    print('%s: %s' % (time.time(), 'calling: connect_future.result()'))
    connect_future.result()
    print('%s: %s' % (time.time(), 'returned: connect_future.result()'))

    message = '%s from %s' % ('test1'if not msg else msg, thing)

    mqtt_connection.publish(topic=topic,
                            payload=message,
                            qos=mqtt.QoS.AT_LEAST_ONCE)

    print('%s: received_all_event.is_set() = %s' % (time.time(), received_all_event.is_set()))

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
