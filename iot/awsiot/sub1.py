#!/usr/bin/python3
#
# sub1.py : An example to use AWS IoT Core Python SDK
#   (aws-iot-device-sdk-python-v2)
#
# Description:
#  * publishes an MQTT message to the sepcified topic.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/01/01 v0.1 Initial version based on AWS examples.
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * ...
#
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import threading

import time
import getopt
import sys
import uuid

import yaml

def handler_conn_interrupted(connection, error, **kwargs):
    print('handler_conn_interrupted: %s : error: %s' % (time.time(), error))
    return


def handler_conn_resumed(connection, return_code, session_present, **kwargs):
    print('handler_conn_resumed: %s : return_code: %s session_present: %s' %
          (time.time(), return_code, session_present))
    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()
        resubscribe_future.add_done_callback(handler_resubscribe_completed)
        return


# registered by in on_connection_resumed handler.
def handler_resubscribe_completed(resubscribe_future):
    print('handler_resubscribe_complete: %s' % (time.time()))
    resubscribe_results = resubscribe_future.result()
    print("%s: Resubscribe results: %s" % (time.time(), resubscribe_results))
    for topic, qos in resubscribe_results['topics']:
        print('topic: %s qos: %s' % (topic, qos))
    return


# registered by mqtt_connection.subscribe() on subscribe time in main.
def handler_message_received(topic, payload, dup, qos, retain, **kwargs):
    msg = payload.decode()
    print('handler_message_received: %s : topic: %s / \'%s\'' %
          (time.time(), topic, msg))
    #received_all_event.set()


def usage():
    print('USAGE: %s:' % (sys.argv[0]))


if __name__ == '__main__':

    conf_file = 'sub1.yaml'

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

    print('Subscribing to topic: %s' % (topic))

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
    #
    # subscriber
    #
    sub_future, pkt_id = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=handler_message_received)
    sub_result = sub_future.result()
    print("Subscribed with %s" % (str(sub_result['qos'])))

    received_all_event.wait()
    print('%s: received_all_event.is_set() = %s' % (time.time(), received_all_event.is_set()))

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
