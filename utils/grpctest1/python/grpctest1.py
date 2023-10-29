#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# grpctest1.py: A junkbox tool for studying gRPC in Python
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/10/14 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# References:
# https://github.com/grpc/grpc/tree/master/examples/python/hellostreamingworld
# https://github.com/techunits/bidirectional-streaming-grpc-sample-python/
import sys
import time
import argparse
import asyncio
import grpc


import echo_pb2
import echo_pb2_grpc

from concurrent import futures

global args

class EchoServer(echo_pb2_grpc.EchoServiceServicer):

    async def Echo(self,
                   request: echo_pb2.EchoRequest,
                   context: grpc.aio.ServicerContext) -> echo_pb2.EchoReply:

        print('Echo() called.')
        if args.debug:
            print(request, dir(request), context)
        for i in range(args.server_iter):
            yield echo_pb2.EchoReply(name = "EchoReply",
                                     type = echo_pb2.commandType.PING,
                                     status = echo_pb2.commandStatus.SUCCESS,
                                     payload = b'number:%d' % (i))


def client_iter():
    for i in range(args.client_iter):
        req = echo_pb2.EchoRequest(name = "EchoRequest",
                                   type = echo_pb2.commandType.PING,
                                   payload = b"1234%d" % (i))
        yield req

async def client() -> None:
    grpc_server = '%s:%d' % (args.host, args.port)
    print(grpc_server)
    async with grpc.aio.insecure_channel(grpc_server) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        print('Calling Echo')
        async for response in stub.Echo(client_iter()):
            print(response)


async def server() -> None:
    server = grpc.aio.server()#futures.ThreadPoolExecutor(max_workers=5))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoServer(), server)
    server.add_insecure_port('%s:%d' % ('0.0.0.0', args.port))
    await server.start()
    await server.wait_for_termination()


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
        asyncio.run(client())

    elif args.mode == 'server':
        print('server')
        asyncio.run(server())

