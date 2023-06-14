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
import etcd3

eps = []

eps.append(etcd3.Endpoint(host='192.168.100.111', port=2379, secure=False))
eps.append(etcd3.Endpoint(host='192.168.100.112', port=2379, secure=False))
eps.append(etcd3.Endpoint(host='192.168.100.113', port=2379, secure=False))

client = etcd3.MultiEndpointEtcd3Client(endpoints=eps, timeout=5, failover=True)

s = client.status()
print('DEBUG: ',
      'leader: ', s.leader, 'index: ', s.raft_index,
      'term: ', s.raft_term, 'version: ', s.version)

for elm in client.members:
    print(elm)
                 
