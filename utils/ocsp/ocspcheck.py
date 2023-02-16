#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ocspcheck.py: A tiny utility for OCSP stapling
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2023/02/15 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * ...
# REFERENCES:
#   * https://www.rfc-editor.org/rfc/rfc6960
#   * Majority of the logic below is from:
#      * https://stackoverflow.com/questions/64436317/how-to-check-ocsp-client-certificate-revocation-using-python-requests-library
import base64
import ssl
import requests
from urllib.parse import urljoin

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509 import ocsp
from cryptography.x509.ocsp import OCSPResponseStatus
from cryptography.x509.oid import ExtensionOID, AuthorityInformationAccessOID

import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ocspcheck.py')
    parser.add_argument('--cert', default=None)
    parser.add_argument('--ocsp_server', default=None)
    parser.add_argument('--issuer', default=None)
    args = parser.parse_args()

    #
    # load (locally stored (normally) client certificate if specified.
    #
    if args.cert:
        #
        # load locally stored (client/server) cerrt
        #
        cert = None
        with open(args.cert, 'rt') as fp:
            cert_pem = fp.read()
            cert = x509.load_pem_x509_certificate(cert_pem.encode('ascii'),
                                                  default_backend())
        if not cert:
            print('ERROR: fail to load cert: %s' % (args.cert))
            sys.exit()
        #
        # extract OCSP server URI
        #
        v = cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
        ocsp_server = v[0].access_location.value
        print('extracted ocsp_server: %s ' % (ocsp_server))
        if args.ocsp_server:
            print('overriding ocsp_server as: %s' % (args.ocsp_server))
            ocsp_server = args.ocsp_server
        #
        # load locally stored issuer cert
        #
        issuer_cert = None
        if args.issuer:
            with open(args.issuer, 'rt') as fp:
                issuer_cert_pem = fp.read()
            issuer_cert = x509.load_pem_x509_certificate(issuer_cert_pem.encode('ascii'), default_backend())
        #
        # create an OCSP request
        #
        builder = ocsp.OCSPRequestBuilder()
        builder = builder.add_certificate(cert, issuer_cert, SHA256())
        req = builder.build()
        req_path = base64.b64encode(req.public_bytes(serialization.Encoding.DER))
        ocsp_req = urljoin(ocsp_server + '/', req_path.decode('ascii'))
        print('OCSP request URL: %s ' % (ocsp_req))
        #
        # send the OCSP request
        #
        ocsp_resp = requests.get(ocsp_req)
        if ocsp_resp.ok:
            ocsp_decoded = ocsp.load_der_ocsp_response(ocsp_resp.content)
            if ocsp_decoded.response_status == OCSPResponseStatus.SUCCESSFUL:
                print('response_status:     %s' % (ocsp_decoded.response_status))
                print('certificate: status: %s' % (ocsp_decoded.certificate_status))
                print('certificate: this_update: %s' % (ocsp_decoded.this_update))
                print('certificate: next_update: %s' % (ocsp_decoded.next_update))
            else:
                print('decoding ocsp response failed: %s' % (ocsp_decoded.response_status))
        else:
            print('fetching ocsp cert status failed with response status: %s ' % (ocsp_resp.status_code))

