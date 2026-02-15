#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# serialization1.py: a script for JSON binary serialization study
#
# License:
#   Apache License, Version 2.0
#
# Dependency
#   * hexdump
#   * cbor2
#   * bson
#   * msgpack
# History:
#   * 2026/02/06 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# References
#  * https://cbor2.readthedocs.io/en/latest/index.html
#  * https://github.com/py-bson/bson
#  * https://github.com/msgpack/msgpack-python/
# TODO
#  * Try protobuf
import sys
import argparse
import pickle
from hexdump import hexdump

args = None

def process_json(data):
    import json
    json_data = json.dumps(data)
    if args.debug:
        print('encoded: len: ', len(json_data))
    return json_data

def process_cbor(data):
    import cbor2
    encoded_data = cbor2.dumps(data)
    if args.debug:
        print('encoded: len: ', len(encoded_data))
        print('encoded: data: ', encoded_data)
        decoded_data = cbor2.loads(encoded_data)
        print('decoded: data: ', decoded_data)
    return encoded_data

def process_bson(data):
    import bson
    encoded_data = bson.dumps(data)
    if args.debug:
        print('encoded: len: ', len(encoded_data))
        print('encoded: data: ', encoded_data)
        decoded_data = bson.loads(encoded_data)
        print('decoded: data: ', decoded_data)
    return encoded_data

def process_msgpack(data):
    import msgpack
    encoded_data = msgpack.packb(data, use_bin_type=True)
    if args.debug:
        print('msgpack: ', encoded_data)
        decoded_data = msgpack.loads(encoded_data, raw=False)
        print('msgpack: decoded: ', decoded_data)
    return encoded_data

def generate_data():
    data = dict()
#    data[''] = 'value1'
#    data['key2'] = {'subkey2': 'subvalue2'}
    data['item'] = [
        {'subkey3': 'subvalue31'},
        {'subkey3': 'subvalue32'},
        {'subkey3': 'subvalue33'},
        {'subkey3': 'subvalue34'},
        {'subkey3': 'subvalue35'}
    ]
    return data

#
# test for reducing iterated keys
#
def process_msgspec(data):
    import msgspec

    class Subkey(msgspec.Struct, array_like=True, omit_defaults=True):
        subkey3: str
        is_active: bool = True

    class Data(msgspec.Struct, array_like=True, omit_defaults=True):
        item: [Subkey]

    data = [Subkey(subkey3=f"subvalue3{i}") for i in range(3)]
    encoded_data = msgspec.msgpack.encode(data)

    if args.debug:
        print('msgspec:')
        # cascaded class definition does not work?
        data1 = [Subkey(subkey3=f"subvalue3{i}") for i in range(3)]
        data = Data(item=data1)
        encoded_data = msgspec.msgpack.encode(data)
        decoded_data = msgspec.msgpack.decode(encoded_data)
        print(decoded_data)

    return encoded_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='otelsrv.py')
    parser.add_argument('--input_file', '-i', default=None)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--dump', action='store_true')
    parser.add_argument('--decode_check', action='store_true')
    args = parser.parse_args()

    # data is 'dict'
    print('input data, pickled dict')
    data = generate_data()
    print('dict: size: ', sys.getsizeof(data))
    hexdump(pickle.dumps(data))

    # JSON
    print('JSON')
    json_data = process_json(data)
    print('len: ', len(json_data))
    hexdump(json_data.encode('utf-8'))

    # COBR
    print('CBOR')
    cbor_data = process_cbor(data)
    print('len: ', len(cbor_data))
    hexdump(cbor_data)

    # BSON
    print('BSON')
    bson_data = process_bson(data)
    print('len: ', len(bson_data))
    hexdump(bson_data)

    # msgpack
    print('msgpack')
    msgpack_data = process_msgpack(data)
    print('len: ', len(msgpack_data))
    hexdump(msgpack_data)

    # msgspec
    print('msgspec')
    msgspec_data = process_msgspec(data)
    print('len: ', len(msgspec_data))
    hexdump(msgspec_data)
