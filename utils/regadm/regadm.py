#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# regadm.py: A tiny utility to manage docker private registry.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/02/13 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Implements commands (list, describe, delete,...)
#   * Integrate garbage collection works
# REFERENCES:
#   * https://stackoverflow.com/questions/43666910/remove-docker-repository-on-remote-docker-registry
#
import sys
import os
import requests
import json
#import yaml
#import pprint
import argparse

REGISTRY=None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='regadm.py')
    parser.add_argument('-u', '--url', default='127.0.0.1:5000')
    parser.add_argument('-o', '--operation', default='LIST')

    args = parser.parse_args()

    REGISTRY=args.url
    OP=args.operation

    print('REGISTRY: %s OP: %s' % (REGISTRY, OP))

    CATALOG_URL='%s/_catalog' % (REG_URL)

    r = requests.get(CATALOG_URL, verify=False)
    repos = json.loads(r.text)
    print('#======================')
    print('# list of repositories ')
    print('#======================')
    #pprint.pprint(r.headers)
    #pprint.pprint(repos)
    for r in repos['repositories']:
        print('%s/%s' % (REGISTRY, r))

    for repo in repos['repositories']:
        print('#======================')
        print('Checking repository: %s' % (repo))
        h = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
        r = requests.get('%s/%s/tags/list' % (REG_URL, repo), verify=False, headers=h)
        images = json.loads(r.text)
        #pprint.pprint(r.headers)
        #pprint.pprint(images['tags'])
        if not images['tags']:
            continue
        for tag in images['tags']:
            print('Checking tag: %s' % (tag))
            h = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
            url = '%s/%s/manifests/%s' % (REG_URL, repo, tag)
            #print('DEBUG: %s'  % (url))
            rr = requests.get(url , verify=False, headers=h)
            #pprint.pprint(rr.headers)
            print('Docker-Content-Digest: %s' % (rr.headers['Docker-Content-Digest']))
            #print(rr.headers)
            #manifest = json.loads(rr.text)
            #pprint.pprint(manifest)
