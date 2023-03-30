#!/usr/bin/env python3

import subprocess
import json
import socket
from contextlib import closing

SUBNET=subprocess.check_output("ip -4 addr show | awk '/inet 192.168./{split($2,a,\".\"); print a[3]}'", shell=True).strip().decode('utf-8')

def get_available_ip(base_ip, subnet):
    ip_parts = base_ip.split(".")
    ip_parts[2] = subnet
    for octet in range(1, 255):
        ip_parts[3] = str(octet)
        candidate_ip = ".".join(ip_parts)
        try:
            with closing(socket.create_connection((candidate_ip, 22), timeout=1)):
                pass
        except (socket.timeout, ConnectionRefusedError, OSError):
            return candidate_ip
    raise ValueError("No available IP addresses in the subnet")

gshortener_ip = get_available_ip("192.168." + SUBNET + ".21", SUBNET)
jenkins_ip = get_available_ip("192.168." + SUBNET + ".22", SUBNET)

inventory = {
    '_meta': {
        'hostvars': {
            'gshortener': {
                'ansible_host': 'gshorthener01.pusula.local',
                'ansible_ssh_host': gshortener_ip,
                'ansible_ssh_user': 'pusula',
                'ansible_ssh_pass': 'pusula+2023'
            },
            'jenkins01': {
                'ansible_host': 'jenkins01.pusula.local',
                'ansible_ssh_host': jenkins_ip,
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
