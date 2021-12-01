import json
import requests
import sys
from argparse import ArgumentParser
from collections import OrderedDict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = '192.168.56.101'
PORT = '443'
USER = 'cisco'
PASS = 'cisco123!'

MANAGEMENT_INTERFACE = "GigabitEthernet1"

url_base = "https://{h}/restconf".format(h=HOST)

headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

url = url_base + "/data/ietf-interfaces:interfaces"

def get_configured_interfaces():
    url = url_base + "/data/ietf-interfaces:interfaces"

    response = requests.get(url,
                        auth=(USER, PASS),
                        headers=headers,
                        verify=False
                        )

    print (url)
    return response.json()["ietf-interfaces:interfaces"]["interface"]

get_configured_interfaces()

def shutdown_int(interface):

    url = url_base + "/data/ietf-interfaces:interfaces/interface={i}".format(i=interface)

    type = 'iana-if.type:ethernetCsmacd'
    if 'Loopback' in interface:
        type = 'iana-if-type:softwareLoopback'

    data = OrderedDict([('ietf-interfaces:interface',
            OrderedDict([
                        ('name', interface),
                        ('type', type),
                        ('enabled', False)
            ])
       )])

    response = requests.put(url,
                            auth=(USER, PASS),
                            headers=headers,
                            verify=False,
                            json=data
                            )
    print(url)
    print(response.txt)

def get_cpu():
    url = url_base + "/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization/five-seconds"

    response = requests.get(url,
                            auth=(USER, PASS),
                            headers=headers,
                            verify=False
                            )

    return response.json()['Cisco-IOS-XE-process-cpu-oper:five-seconds']

get_cpu()