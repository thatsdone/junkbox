#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# etcd3-multiclient: A test chunk to connect multiple etcd3 servers using python-etcd3
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/06/14 v0.1 Initial version
#   * 2023/09/01 v0.2 Add several sample operations
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# Dependencies:
#   * python-etcd3 : https://github.com/kragniz/python-etcd3/
# Special Note:
#   As of June 14, 2023, https://pypi.org/project/etcd3/ distributes 0.12.0.
#   But the version does not contain multiple etcd connection support.
#   Download master branch from the git repository. I used the below:
#   $ git log --oneline -n 1
#   e58a899 (HEAD -> master, origin/master, origin/HEAD) Merge pull request #1958 from jkawamoto/grpc
import sys
import argparse
import etcd3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='etcd3-test1.py')
    parser.add_argument('-e', '--endpoints', nargs="*", default=None)
    parser.add_argument('-o', '--op', default='status')
    parser.add_argument('-w', '--watch_key',default='/key1')
    parser.add_argument('-c', '--watch_count', type=int, default=10)
    parser.add_argument('-t', '--timeout', type=int, default=5)
    args = parser.parse_args()

    eps = []
    if args.endpoints:
        for ep in args.endpoints:
            eps.append(etcd3.Endpoint(host=ep.split(':')[0], port=int(ep.split(':')[1]), secure=False))
    else:
        print('Specify -e / --endpoints')
        sys.exit()

    client = etcd3.MultiEndpointEtcd3Client(endpoints=eps,
                                            timeout=args.timeout,
                                            failover=True)
    if args.op == 'status':
        print(eps)
        #
        for elm in client.members:
            print(elm)
        #
        s = client.status()
        print('leader: ', s.leader,
              'index: ', s.raft_index,
              'term: ', s.raft_term,
              'version: ', s.version)

    if args.op == 'watch':
        print('Watching key: %s for %d events.' % (args.watch_key, args.watch_count))
        watch_count = 0
        events_iterator, cancel = client.watch(args.watch_key)
        for event in events_iterator:
            print(event._event)
            watch_count += 1
            if watch_count >= args.watch_count:
                cancel()

    if args.op == 'client':
        #print(args.watch_key)
        print('# get: key: %s' % (args.watch_key))
        print(client.get(args.watch_key))
        v = 'value1'
        print('# put: key: %s value: %s' % (args.watch_key, v))
        print(client.put(args.watch_key, v))
        print('# get: key: %s' % (args.watch_key))
        print(client.get(args.watch_key))
        print('# delete: key: %s' % (args.watch_key))
        print(client.delete(args.watch_key))
        print('# get: key: %s' % (args.watch_key))
        print(client.get(args.watch_key))
