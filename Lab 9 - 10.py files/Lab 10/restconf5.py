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

url_base = "https://192.168.56.101/restconf"

headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

def get_configured_interfaces():
    url = url_base + "/data/ietf-interfaces:interfaces"

    response = requests.get(url,
                        auth=(USER, PASS),
                        headers=headers,
                        verify=False
                        )

    print (url)
    return response.json()["ietf-interfaces:interfaces"]["interface"]

#get_configured_interfaces()

def shutdown_int(interface):

    url = url_base + "/data/ietf-interfaces:interfaces/interface=Loopback100"

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
    print(response.text)

#shutdown_int('Loopback100')

def get_cpu():
    url = url_base + "/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization/five-seconds"

    response = requests.get(url,
                            auth=(USER, PASS),
                            headers=headers,
                            verify=False
                            )

    return response.json()['Cisco-IOS-XE-process-cpu-oper:five-seconds']

#get_cpu()

def get_mem():
    url = url_base + "/data/Cisco-IOS-XE-memory-oper:memory-statistics/memory-statistic=Processor"

    response = requests.get(url,
                            auth=(USER, PASS),
                            headers=headers,
                            verify=False
                            )
    data = response.json()["Cisco-IOS-XE-memory-oper:memory-statistic"]

    print("Name: ", data["name"])
    used,free = 0,0
    try:
        used = int(data["used-memory"])
        free = int(data["free-memory"])
    except KeyError:
        print("Json Error")
    print()


    return (used/(used+free)) * 100, (free/(used+free)) * 100

#get_mem()

def get_int_state():
    url = 'https://192.168.56.101/restconf/data/ietf-interfaces:interfaces-state'

    response = requests.get(url,
                        auth=(USER, PASS),
                        headers=headers,
                        verify=False
                        )
    
    phys = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['phys-address']
    speed = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['speed']
    dis = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['discontinuity-time']
    inoct = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['in-octets']
    inuni = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['in-unicast-pkts']
    inbro = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['in-broadcast-pkts']
    inmulti = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['in-multicast-pkts']
    outoct = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['out-octets']
    outuni = response.json()['ietf-interfaces:interfaces-state']['interface'][2]['statistics']['out-unicast-pkts']
    
    print (phys)
    print (speed)
    print (dis)
    print (inoct)
    print (inuni)
    print (inbro)
    print (inmulti)
    print (outoct)
    print (outuni)

get_int_state()