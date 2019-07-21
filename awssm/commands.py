from invoke import task
import os
import boto3
import base64
from botocore.exceptions import ClientError
import pprint
import json

DELIM='/'

@task
def list(ctx, service):
    """list secrets in <service> or all"""

    # Create a Secrets Manager client
    session = boto3.Session()
    secrets = boto3.client('secretsmanager')
    try:
        resp = secrets.list_secrets()
    except ClientError as e:
        raise e
    service = '' if service == 'all' else service + DELIM

    if service == 'all':
        keys = [key for key in resp['SecretList']]
        print('All Services')
        # for key in keys:
        #     print(key['Name'])
    else:
        keys = [key for key in resp['SecretList'] if service in key['Name']]

        print("{:{wid}} {}".format('KEY', 'MODIFIED', wid=col1))
        for key in keys:
            print("{:{wid}} {:%Y-%m-%d %H:%M:%S}".format(key['Name'].split(DELIM,1)[1], key['LastChangedDate'], wid=col1))

    if keys:
        col1=max(len(key['Name'].split(DELIM,1)[1]) for key in keys) + 5

    else:
        print('awssm: Specify <service> or all')

@task
def read(ctx, service, key):
    """read key value from secrets manager"""
    session = boto3.Session()
    secrets = boto3.client('secretsmanager')
    keyval = service + DELIM + key
    try:
        resp = secrets.get_secret_value(SecretId=keyval)
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in resp:
            print(eval(resp['SecretString'])[key])
        else:
            print(eval(base64.b64decode(resp['SecretBinary'])))

@task
def write(ctx, service, key, value):
    """write key/value under a service path"""
    binary = False
    session = boto3.Session()
    secrets = boto3.client('secretsmanager')
    keyval = service + DELIM + key
    if value == '-':
        value = sys.stdin.buffer.read()
        binary = True
    try:
        response = secrets.describe_secret(SecretId=keyval)
        if binary == True:
            response = client.update_secret(SecretId=keyval, SecretString=value)
        else:
            response = client.update_secret(SecretId=keyval, SecretBinary=value)
    except ClientError as e:
        # this is a new secrets
        if binary == True:
            response = secrets.create_secret(Name=keyval, SecretString=value)
        else:
            response = secrets.create_secret(Name=keyval, SecretBinary=value)
