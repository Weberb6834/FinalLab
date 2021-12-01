from ncclient import manager
import xml.dom.minidom as p
import xmltodict

m = manager.connect(
host="192.168.56.101",
port=830,
username="cisco",
password="cisco123!",
hostkey_verify=False
)

netconf_filter = """
<filter>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Loopback0</name>
        </interface>
    </interfaces>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Loopback0</name>
        </interface>
    </interfaces-state>
</filter>
"""

print('############################')
netconf_reply = m.get(netconf_filter)
intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"] ["data"]
intf_config = intf_details ["interfaces"] ["interface"]
intf_info = intf_details ["interfaces-state"] ["interface"]

print("")
print("Interface Details:")
print("   IPv4: {}".format(intf_config["ipv4"]["address"]["ip"]))
print("   Type: {}".format(intf_config["type"]["#text"]))
print("   MAC Address: {}".format(intf_config["phys-address"]))
print("   Packets Input: {}".format(intf_config["statistics"]["in-unicast-pkts"]))
print("   Packets Output: {}".format(intf_config["statistics"]["out-unicast-pkts"]))
print("   Admin-Status:  {}".format(intf_config["admin-status"]))
print("   Oper-Status:  {}".format(intf_config["oper-status"]))
