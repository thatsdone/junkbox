#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# slack-log-reader.py: A tiny utility to work with slack messaging
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/05/09 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# REFERENCES:
#   * https://api.slack.com/apis
import sys
import argparse
import json
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='slack-log-reader.py')
    parser.add_argument('-f', '--filename', default=None)
    args = parser.parse_args()

    filename  = args.filename
    if not filename:
        print('Specify log data filanem via -f')
        sys.exit()

    with open(filename, 'r') as fp:
        data = json.load(fp)

    msgs = []

    count=0
    for elm in data['messages']:
        text = elm['text'].split('|')[0].replace('<', '').replace('>', '')
        msgs.append({'ts': elm['ts'], 'text': text})
        count += 1
        print(datetime.datetime.fromtimestamp(int(float(elm['ts']))), elm['ts'], text)

    print('total: %d ' % (count))

    #for m in sorted(msgs, key=lambda record: record['ts']):
    #    print(datetime.datetime.fromtimestamp(int(float(m['ts']))), m['text'])

    a= sorted(msgs, key=lambda record: record['ts'])
    print(datetime.datetime.fromtimestamp(int(float(a[0]['ts']))),
          a[0]['ts'],
          datetime.datetime.fromtimestamp(int(float(a[-1]['ts']))),
          a[-1]['ts'])
