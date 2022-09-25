#!/usr/bin/python3
#
# openstack-example : A simple example of OpenStack Python Clients
#
# Description:
#   A simple example of OpenStack Python Clients
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/08/28 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# TODO:
#  Add more examples...
import sys
import os
# import argparse


class OSExample:
    def get_os_credentials(self):
        #
        # get authentication info. from environment variables
        #
        self.os_auth_url = os.environ['OS_AUTH_URL']
        self.os_username = os.environ['OS_USERNAME']
        self.os_password = os.environ['OS_PASSWORD']
        self.os_project_name = os.environ['OS_PROJECT_NAME']
        self.os_project_id = os.environ['OS_PROJECT_ID']
        self.os_project_domain_name = os.environ['OS_PROJECT_DOMAIN_NAME']
        self.os_user_domain_name = os.environ['OS_USER_DOMAIN_NAME']
        self.os_endpoint_type = 'adminURL'
        self.os_identity_api_version = '3'
        self.os_compute_api_version = '2.1'
        self.os_image_api_version = '2'
        self.cert_verify = False

    def example(self):
        from keystoneauth1.identity import v3
        from keystoneauth1 import session
        from keystoneclient.v3 import client as keystoneclient
        #
        from novaclient import client as novaclient
        #
        from glanceclient import client as glanceclient

        self.auth = v3.Password(auth_url=self.os_auth_url,
                                username=self.os_username,
                                password=self.os_password,
                                project_name=self.os_project_name,
                                project_id=self.os_project_id,
                                project_domain_name=self.os_project_domain_name,
                                user_domain_name=self.os_user_domain_name)
        # create a session object
        sess = session.Session(auth=self.auth, verify=self.cert_verify)

        # create keystone client instance
        kclient = keystoneclient.Client(session=sess)

        # get user_id of the current user from auth
        user_id = self.auth.get_user_id(sess)
        print('user id(auth) : %s' % (user_id))
        # get user related information from keystone client
        # especially, domain id is important
        user = kclient.users.get(user_id)
        print('name : %s' % (user._info['name']))
        print('user id : %s' % (user._info['id']))
        print('domain id : %s ' % (user._info['domain_id']))
        # print('description : %s ' % (user._info['description']))

        # list projects that the given user has membership
        projects = kclient.projects.list(user=user)
        for project in projects:
            print(project._info['name'], project._info['id'])


#
# main
#
if __name__ == "__main__":

    ose = OSExample()

    ose.get_os_credentials()
    ose.example()
