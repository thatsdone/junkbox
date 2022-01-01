# AWS IoT Core Python SDK v2 examples

## Description

* sub1.py : A simple subscriber
  * Connects to AWS IoT Core, subscribes to a topic (default: topic_1) and
    keep receiving messages.
* pub1.py : A simple publisher
  * Connects to AWS IoT Core, publishes a specified message to a topic
    (default: topic_1) and exits immediately.
* example1.yaml : An example configuration file for pub1.py and sub1.py
```
creds:
  thing = '12345678-thing1'
  cred_dir: 'CRED_DIR'
  root_ca: 'AmazonRootCA1.pem'
  endpoint: 'xxxxxxxxxxxxxx-ats.iot.ap-northeast-1.amazonaws.com'
  ca_certificate: '12345678-certificate.pem.crt'
  private_key: '12345678-private.pem.key'
  topic: '12345678/abcdefgh/topic_1'
```
  * cred_dir holds all the credential files.

## Options

  -f : configulation file (e.g., example1.yaml)
  -e : endpoint
  -c : ca_certificate
  -t : topic
  -m : message (pub1.py only)
  -h : help

## TODO
* Add an option for cred_dir
* Add an option for thing name
* Write helper scripts to generate and setup credentials.
* Write other MQTT implementation bindings (e.g., Eclipse Paho)
