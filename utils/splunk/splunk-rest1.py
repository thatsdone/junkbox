#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# splunk-rest1.py: A tiny exercise tool to query to Spkunk via bare REST API
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2024/01/20 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys
import argparse
import requests
import urllib3
from lxml import etree
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='splunk-rest1.py')
    parser.add_argument('-h', '--host', default=None)
    parser.add_argument('-p', '--port', type=int, default=8089)
    parser.add_argument('--insecure', action='store_true')
    parser.add_argument('-U', '--username', default='admin')
    parser.add_argument('-P', '--password', default=None)
    parser.add_argument('-T', '--token', default=None)
    parser.add_argument('-S', '--search', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    #
    if not args.host:
        print('Specify Splunk server IP (--host/-h)')
        sys.exit()
    if not args.search:
        print('Specify search string (--search/-S)')
        sys.exit()
    if not args.password and not args.token:
        print('Specify password(--password/-P) or token(--token/-T)')
        sys.exit()

    if args.insecure:
        urllib3.disable_warnings()
    #
    base_url='https://%s:%d' % (args.host, args.port)
    #
    auth_url='%s/servicesNS/admin/search/auth/login' % base_url
    search_url='%s/services/search/jobs' % base_url

    auth={'username': args.username, 'password': args.password}
    resp = requests.get(auth_url, data=auth, verify=False)

    if resp.status_code != 200:
        print('Failed to authenticate: %s' % (resp.status_code))
        if args.debug:
            print(resp.text)
        sys.exit()

    root = etree.fromstring(resp.text)
    if args.debug:
        print(root)
    # lookup sessionKey
    session_key = None
    for child in root:
        #print(child, child.tag, child.text)
        if child.tag == 'sessionKey':
            if args.debug:
                print(child.text)
            session_key = child.text
    if not session_key:
        print('Could not get a session key:  %s' % (resp.text))
        sys.exit()

    # execute search
    auth={'Authorization': 'Splunk %s' % session_key}
    search = {
        "search": 'search %s' % args.search,
        "exec_mode": "oneshot",
        "output_mode": "json"
        }
    resp = requests.post(search_url, headers=auth, data=search, verify=False)

    if args.debug:
        print(resp.status_code)
        print(json.dumps(resp.text))
    print(resp.text)
