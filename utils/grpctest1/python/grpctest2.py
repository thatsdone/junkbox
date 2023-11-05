#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# grpctest2.py: A junkbox tool for studying gRPC in Python not using async
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/11/04 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# References:
# https://github.com/grpc/grpc/tree/master/examples/python/hellostreamingworld
# https://github.com/techunits/bidirectional-streaming-grpc-sample-python/
import sys
import time
import argparse
import grpc

import echo_pb2
import echo_pb2_grpc

from concurrent import futures

global args

class EchoServer(echo_pb2_grpc.EchoServiceServicer):

    # This is called only after the client called 'stub.Echo()'.
    def Echo(self, request_iterator, context):
        print('Echo() called.')
        for request in request_iterator:
            for i in range(args.server_iter):
                print('got a request', request)
                yield echo_pb2.EchoReply(name = "EchoReply",
                                         type = echo_pb2.commandType.PING,
                                         status = echo_pb2.commandStatus.SUCCESS,
                                         payload = b'number:%d' % (i))
                print('sleep 1 second')
                time.sleep(1)


def client_iter():
    print('client_iter() called. client_iter: %d' % (args.client_iter))
    for i in range(args.client_iter):
        print('client_iter(): i= %d' % (i))
        req = echo_pb2.EchoRequest(name = "EchoRequest",
                                   type = echo_pb2.commandType.PING,
                                   payload = b"1234%d" % (i))
        print('yielding a req')
        yield req
        print('sleep 2 seconds')
        time.sleep(2)

def client():
    grpc_server = '%s:%d' % (args.host, args.port)
    print(grpc_server)
    with grpc.insecure_channel(grpc_server) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        #print('sleep 10 seconds')
        #time.sleep(10)
        print('Calling Echo')
        for response in stub.Echo(client_iter()):
            print('got a response.')
            print(response)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoServer(), server)
    server.add_insecure_port('%s:%d' % ('0.0.0.0', args.port))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='grpctest1.py')
    parser.add_argument('-m', '--mode', default='server')
    parser.add_argument('-p', '--port', type=int, default=50051)
    parser.add_argument('--server_iter', type=int, default=3)
    parser.add_argument('--client_iter', type=int, default=2)
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.mode == "client":
        print('client')
        client()

    elif args.mode == 'server':
        print('server')
        server()

