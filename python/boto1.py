#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# boto1.py: A tiny bot3 example showing differences between resource and client
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/01/28 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
#import sys
import boto3
#from boto3.session import Session
import argparse
#import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='boto1.py')
    parser.add_argument('--use_client', action='store_true')
    parser.add_argument('--service', default='dynamodb')
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--region', default='ap-northeast-1')
    parser.add_argument('--access_key_id', default=None)
    parser.add_argument('--secret_access_key', default=None)
    parser.add_argument('--profile', default=None)
    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile,
                            region_name=args.region,
                            aws_access_key_id=args.access_key_id,
                            aws_secret_access_key=args.secret_access_key)

    endpoint_url = 'http://%s:%d' % (args.host, args.port) if args.host and args.port else None
    sclient = None

    if args.use_client:
        sclient = session.client(service_name=args.service,
                                  endpoint_url = endpoint_url)
        # dynamodb
        resp = sclient.list_tables()
    else:
        sclient = session.resource(args.service,
                                   endpoint_url = endpoint_url)
        # dynamodb
        resp = sclient.tables.all()

    print(resp)

    for item in resp:
        print(item)
