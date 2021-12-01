from ncclient import manager
import xml.dom.minidom as p
import xmltodict
import routers

m = manager.connect(**routers.router)

netconf_template = open("config_templ_ietf_interface.xml").read()

netconf_payload = netconf_template.format(int_name="Loopback",
                                            int_num="1",
                                            int_desc="Configured by NETCONF With a Template",
                                            ip_address="100.1.1.1",
                                            subnet_mask="255.255.255.0"
                                            )
print("Configuration Payload:")
print("----------------------")
print(netconf_payload)

print('#'*80)

netconf_reply = m.edit_config(target="running", config=netconf_payload)

print(netconf_reply)