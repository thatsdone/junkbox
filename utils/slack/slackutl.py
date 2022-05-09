#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# slackutl.py: A tiny utility to work with slack messaging
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/05/09 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * ...
# REFERENCES:
#   * 
#
import sys
import os
import time
import requests
import json
import yaml
import argparse

channel = None
ts = None
#
#
#
if __name__ == "__main__":

    token = None
    channel = None
    ts = None
    
    parser = argparse.ArgumentParser(description='slackutl.py')
    parser.add_argument('-c', '--config', default='slackutl.yaml')
    parser.add_argument('-u', '--url', default=None)
    parser.add_argument('-C', '--channel', default=None)
    parser.add_argument('-T', '--token', default=None)
    parser.add_argument('-t', '--timestamp', default=None)
    parser.add_argument('-o', '--operation', default='history')
    parser.add_argument('-m', '--message', default=None)
    parser.add_argument('-k', '--keyvalues', default=None)
    args = parser.parse_args()

    if not args.url and not args.channel and not args.token:
        if not os.path.isfile(args.config):
            print('ERROR: config file does not exist. %s' % (args.config))
            sys.exit()
    
    try:
        conf = None
        with open(args.config, 'r') as ymlconf:
            conf=yaml.load(ymlconf, Loader=yaml.SafeLoader)

        if args.channel:
            channel = args.channel            
        elif not args.channel and 'channel' in conf.keys():
            channel = conf['channel']

        if not args.token and 'token' in conf.keys():
            token = conf['token']
    except Exception as e:
        print('Error processing %s. %s' % (args.config, e))
        sys.exit()
    #
    #
    #
    if not channel:
        print('Specify channel.')
        sys.exit()
        
    if not args.timestamp:
        ts = time.time()
        #print('DEBUG: Using current time for ts: %s' % (ts))
    else:
        ts = args.timestamp

    header={
        "Authorization": "Bearer {}".format(token)
    }
    payload = dict()

    if args.operation == 'history':
        if not ts:
            print('Specify ts (timestamp) of the message to delete.')
            sys.exit()
        url = "https://slack.com/api/conversations.history"
        payload['channel']  = channel
        payload['ts']  = ts
        
    elif args.operation == 'write':
        if not args.message:
            print('Specify message to write.')
            sys.exit()
        url = "https://slack.com/api/chat.postMessage" 
        msg = '%s' % (args.message)
        payload['channel'] = channel
        payload['text'] = message

    elif args.operation == 'delete':
        if not ts:
            print('Specify ts (timestamp) of the message to delete.')
            sys.exit()
        url = 'https://slack.com/api/chat.delete'
        payload['channel'] = channel
        payload['ts'] = ts

    elif args.operation == 'generic':
        if not args.url:
            print('Specify at least url via -u.')
            sys.exit()
        if not args.keyvalues:
            print('Specify at least url via -k or --keyvalues.')
            sys.exit()
        for kv in args.keyvalues.split(','):
            (key, value) = kv.split('=')
            print(key, value)
            payload[key] = value
    #
    res = requests.post(url, headers=header, params=payload)
    #
    print(res.text)
    #
    if args.operation == 'history':
        with open('slackutl-%s.json' % (ts), 'wt') as fp:
            fp.write(res.text)
