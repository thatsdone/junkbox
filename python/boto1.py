import boto3
from boto3.session import Session
#import sys
import argparse
#import csv
#import datetime
#import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='boto1.py')
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--region', default='ap-northeast-1')
    parser.add_argument('--access_key_id', default='dumy')
    parser.add_argument('--secret_access_key', default='dumy')
    args = parser.parse_args()

    session = boto3.Session()
    dynamodb = session.resource('dynamodb',
                                region_name=args.region,
                                aws_access_key_id=args.access_key_id,
                                aws_secret_access_key=args.secret_access_key,
                                endpoint_url = 'http://%s:%d' % (args.host, args.port))
    resp = dynamodb.tables.all()
    print(resp)
    for item in resp:
        print(item)
