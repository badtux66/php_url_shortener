#!/usr/bin/env python3

import subprocess
import json

SUBNET=subprocess.check_output("ip -4 addr show | awk '/inet 192.168./{split($2,a,\".\"); print a[3]}'", shell=True).strip().decode('utf-8')

inventory = {
    '_meta': {
        'hostvars': {
            'gshortener': {
                'ansible_host': 'gshorthener01.pusula.local',
                'ansible_ssh_host': '192.168.' + SUBNET + '.21',
                'ansible_ssh_user': 'pusula',
                'ansible_ssh_pass': 'pusula+2023'
            },
            'jenkins01': {
                'ansible_host': 'jenkins01.pusula.local',
                'ansible_ssh_host': '192.168.' + SUBNET + '.22',
                'ansible_ssh_user': 'pusula',
                'ansible_ssh_pass': 'pusula+2023'
            }
        }
    },
    'web_nodes': {
        'hosts': ['gshortener']
    },
    'jenkins_nodes': {
        'hosts': ['jenkins01']
    },
    'all': {
        'children': ['web_nodes', 'jenkins_nodes']
    }
}

print(json.dumps(inventory))
