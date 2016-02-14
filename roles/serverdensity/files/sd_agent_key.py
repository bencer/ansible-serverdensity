#!/usr/bin/env python3

import argparse
import requests
import json
import os
import sys

token = os.environ['SD_TOKEN']

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n','--name', action='store', help='Device name')
parser.add_argument('-g','--group', action='store', help='Device group name')
parser.add_argument('-ec2','--ec2_instance_id', action='store', help='AWS EC2 instance ID')
parser.add_argument('-o','--override', action='store_true',
                    help='Override existing device')
parser.add_argument('-c','--check', action='store', help='Check agentKey exists')

args = parser.parse_args()

required_fields = json.dumps(['_id', 'name', 'type', 'agentKey', 'group',
                              'publicIPs', 'privateIPs',
                              'updatedAt', 'createdAt', 'accountId',
                              'deleted'])

myfilter = {}

if args.check:
    myfilter = json.dumps({'agentKey': args.check,
                           'type': 'device'})

if args.override:
    myfilter = json.dumps({'name': args.name, 'group': args.group,
                           'type': 'device'})

if args.ec2_instance_id:
    myfilter = json.dumps({'provider': 'amazon', 'providerId': args.ec2_instance_id,
                           'type': 'device'})

if myfilter:
    api_response = requests.get(
        'https://api.serverdensity.io/inventory/resources',
        params = {
            'token': token,
            'filter': myfilter,
            'fields': required_fields
        }
    )

    json_data = json.loads(api_response.text)

    if len(json_data) > 0:
        print(json.dumps(json_data[0]))
        sys.exit()
    else:
        sys.exit(1)

api_response = requests.post(
    'https://api.serverdensity.io/inventory/devices/',
    params = {
        'token': token
    },
    data = {
        "name": args.name,
        "group": args.group,
    }
)

json_data = json.loads(api_response.text)
print(json.dumps(json_data))
