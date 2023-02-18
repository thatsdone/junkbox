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
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', type=int, default=443)
    parser.add_argument('--cert', default=None)
    parser.add_argument('--ocsp_server', default=None)
    parser.add_argument('--issuer', default=None)
    parser.add_argument('--debug', action='store_true')
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
    else:
        conn = ssl.create_connection((args.host, args.port))
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sock = context.wrap_socket(conn, server_hostname=args.host)
        certDER = sock.getpeercert(True)
        certPEM = ssl.DER_cert_to_PEM_cert(certDER)
        cert = x509.load_pem_x509_certificate(certPEM.encode('ascii'), default_backend())

    ocsp_server = None
    issuer_url = None
    issuer_cert = None
    #
    # Lookup Authority Information and extract Issuer/OCSP
    #
    v = cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
    for elm in v:
        if elm.access_method == AuthorityInformationAccessOID.OCSP:
            print('Found: OCSP', elm.access_location.value)
            ocsp_server = elm.access_location.value

        elif elm.access_method == AuthorityInformationAccessOID.CA_ISSUERS:
            print('Found: Issuer', elm.access_location.value)
            issuer_url = elm.access_location.value

    if args.ocsp_server:
        print('overriding ocsp_server as: %s' % (args.ocsp_server))
        ocsp_server = args.ocsp_server

    #
    # load ssuer cert
    #
    if not args.issuer:
        issuer_response = requests.get(issuer_url)
        if issuer_response.ok:
            issuerDER = issuer_response.content
            issuerPEM = ssl.DER_cert_to_PEM_cert(issuerDER)
            issuer_cert = x509.load_pem_x509_certificate(issuerPEM.encode('ascii'), default_backend())
        else:
            print('GET Issuer cert faile.')
            sys.exit()
    else:
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

