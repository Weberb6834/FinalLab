import time
import json
import requests
requests.packages.urllib3.disable_warnings()
from netmiko import ConnectHandler
import myParamiko as m
import paramiko
import time
# Genie import
from genie.conf import Genie

# import the genie libs
from genie.libs import ops # noqa

# Parser import
from genie.libs.parser.iosxe.show_interface import ShowIpInterfaceBrief

# Import Genie Conf
from genie.libs.conf.interface import Interface

class Monitor():

    def setup(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.device_list = []
        str = ""
        for device in genie_testbed.devices.values():
            try:
                device.connect()
            except Exception as e:
                print("Failed to establish connection to '{}'".format(
                    device.name))
                str += "\nFailed to establish connection to "+ device.name

            self.device_list.append(device)

        return str

    ################################################################################################
    ################################################################################################
    ################################################################################################

    def learn_interface(self):
        
        url = "https://192.168.56.106/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2/ietf-ip:ipv4/address="
        
        #r1_url = "https://192.168.56.104/restconf/data/ietf-interfaces:interfaces"
        headers = {"Accept": "application/yang-data+json",
           "Content-type":"application/yang-data+json"
           }
        HOST = '192.168.56.106'
        PORT = '443'
        USER = 'cisco'
        PASS = 'cisco123!'
        resp = requests.get(url,
                        auth=(USER, PASS),
                        headers=headers,
                        verify=False
                        )

        
        ################################################################################################
        ################################################################################################
        ################################################################################################

        response_json = resp.json()
        
    
        ip_addr = response_json['ietf-ip:address'][0]['ip']
    

        r1_url ="https://192.168.56.104/restconf/data/ietf-interfaces:interfaces/interface=Loopback56/description"
        USER1 = 'cisco'
        PASS1 = 'cisco123!'
        resp1 = requests.get(r1_url,
                        auth=(USER1, PASS1),
                        headers=headers,
                        verify=False
                        )
        response_json1 = resp1.json()
        old_ip = response_json1['ietf-interfaces:description'] #getting old ip address

     ################################################################################################
     ################################################################################################
     ################################################################################################

        if old_ip == ip_addr :
            print ("IT WORKED")
            print ("Current IP " + ip_addr)
            
        else:
            print ("Old Ip Address " + old_ip)
            print ("New Ip Address " + ip_addr)

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            router = {'hostname': '192.168.56.104','port': '22', 'username':'cisco', 'password':'cisco123!'}
            
            print(f'Connecting to {router["hostname"]}')
            ssh_client.connect(**router, look_for_keys=False, allow_agent=False) 
            shell = ssh_client.invoke_shell()

            shell.send('enable\n')
            shell.send('cisco123!\n')
            shell.send('conf t\n')
            shell.send('no crypto isakmp key cisco address '+ old_ip +'\n')
            shell.send('crypto isakmp key cisco address '+ ip_addr +'\n')
            shell.send('crypto map Crypt 10 ipsec-isakmp\n')
            shell.send('no set peer '+ old_ip +'\n')
            shell.send('set peer '+ ip_addr +'\n')
            shell.send('exit\n')
            shell.send('int lo56\n')
            shell.send('description '+ ip_addr + '\n')
            shell.send('end\n')
            time.sleep(2)
            if ssh_client.get_transport().is_active() == True:
                print('Closing connection')
                ssh_client.close()
        return (old_ip,ip_addr)


if __name__ == "__main__":
    # Test Functions
    mon = MonitorInterfaces()
    #mon.setup('testbed/routers.yml')
    intf = mon.learn_interface()
    print(intf)
