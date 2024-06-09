#!/usr/bin/python3
#
# k8sutil : A small kubernetes API utility mostly for study
#
# Description:
#   An exercise/study script for calling kubernetes REST API from python.
#   Never completes (probably).
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2024/06/09 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
# References:
#   * https://stackoverflow.com/questions/76031802/python-kubernetes-client-equivalent-of-kubectl-api-resources-namespaced-false
#   * raw request (javascript case)
#     * https://github.com/kubernetes-client/javascript/pull/181/files
# TODO:
#   * Enable calling raw API perhaps using requests
import sys, os, getopt, errno
import argparse
import json
import datetime
import requests

from kubernetes import client, config

global args

def list_apis():
    print('# ApisApi ')
    apigroups = client.ApisApi().get_api_versions().groups

    for api in apigroups:
        #print(api)
        print(api.name, api.preferred_version.group_version)

def list_standard_apis():
    # TODO(thatsdon): other standard (not extension) APIs.

    cclient = client.CoreV1Api()
    aclient = client.AppsV1Api()
    jclient = client.BatchV1Api()

    print('# CoreV1')
    r = cclient.get_api_resources()
    #print(r)
    for res in r.resources:
        print(r.group_version, res.name, res.kind)

    print('# AppV1')
    r = aclient.get_api_resources()
    for res in r.resources:
        print(r.group_version, res.name, res.kind)

    print('# BatchV1')
    r = aclient.get_api_resources()
    for res in r.resources:
        print(r.group_version, res.name, res.kind)

def list_extensions():
    print('# ApiExtensionsV1 ')

    #r = client.ApiextensionsV1Api().list_custom_resource_definition()
    #print(r)
    #sys.exit()
    
    for res in r.items:
        print(res.spec.group, res.spec.names.singular)
    #print(r)

def list_resource_apis():
    # TODO(thatsdone): This returns 404.
    r = client.ResourceApi().get_api_group()
    print(type(r), r)

def get_custom_object(group, version):
    #print(dir(client.CustomObjectsApi))
    return client.CustomObjectsApi().get_api_resources(group=group,
                                                       version=version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='k8sutil.py')
    parser.add_argument('--kubeconfig', default=None)
    parser.add_argument('--op', default='api-resources')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    kubeconfig = None
    if args.kubeconfig:
        kubeconfig = args.kubeconfig
    elif os.getenv('KUBECONFIG', None):
        kubeconfig = os.getenv('KUBECONFIG')
    if not kubeconfig:
        print('Specify KUBECONFIG or --kubeconfig')
        sys.exit()

    config.load_kube_config(kubeconfig)
    
    if args.op == 'list_apis':
        list_apis()

    elif args.op == 'list_standard_apis':
        list_standard_apis()

    elif args.op == 'list_extensions':
        list_extensions()
        
    elif args.op == 'get_custom_object':
        group='batch'
        version='v1'
        print(get_custom_object(group, version))

    # forget this
    #print(dir(client.V1APIResourceList))
    #r = client.V1APIResourceList(group_version='v1', resources='batch')
    #print(type(r), r)
       

    
    
