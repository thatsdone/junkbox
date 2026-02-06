#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# serialization1.py: a script for JSON binary serialization study
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2026/02/06 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
data = dict()
data['key1'] = 'value1'
data['key2'] = {'subkey2': 'subvalue2'}
data['key3'] = [
    {'subkey3': 'subvalue31'},
    {'subkey3': 'subvalue32'},
    {'subkey3': 'subvalue33'},
    {'subkey3': 'subvalue34'},
    {'subkey3': 'subvalue35'}
    ]

import json
print('JSON')
print('len: ', len(json.dumps(data)))

import cbor2
print('CBOR')
encoded_data = cbor2.dumps(data)
print('len: ', len(encoded_data))
print('CBOR: ', encoded_data)
decoded_data = cbor2.loads(encoded_data)
print('CBOR: decoded: ', decoded_data)

import bson
print('BSON')
encoded_data = bson.dumps(data)
print('len: ', len(encoded_data))
print('BSON: ', encoded_data)
decoded_data = bson.loads(encoded_data)
print('BSON: decoded: ', decoded_data)


import msgpack
print('msgpack')
encoded_data = msgpack.packb(data, use_bin_type=True)
print('len: ', len(encoded_data))
print('msgpack: ', encoded_data)
decoded_data = msgpack.loads(encoded_data, raw=False)
print('msgpack: decoded: ', decoded_data)

