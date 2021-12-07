# 381 Final - Disaster Monitoring using Genie Bot
<img src='images/header.png' width=70% />

>This Image shows the topology we used to in our project, we used vitural CSRV1000 routers representing our Headquarters and Branch Routers. Ran the virtual machines on Virtual Box VM. Router 1 (HQ) and Router 2 (Branch), have a vpn connection allowing them access with eachother.

In the project we use multiple automation & programibility methods to monitor, configure and print, router configurations in our lab enviorment. We use methods such as RestConf, Paramiko, Ansible and Genie bot to achieve our goals. The main goal of the lab was to monitor g/2 interface on Router 2 (Branch) and check for a DHCP change of the ip on the interface. If an address change is detected, the bot monitoring the interface updates the old ip address in the vpn configuration on Router 1 (HQ), and removes the old vpn configuration.

### Restconf for Disaster monitoring

1. Library for the interface

          url = "https://192.168.56.106/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2/ietf-ip:ipv4/address="
        
2. Headers used for formatting

          headers = {"Accept": "application/yang-data+json",
           "Content-type":"application/yang-data+json"
           
3. Formatting message output

          response_json = resp.json()
          ip_addr = response_json['ietf-ip:address'][0]['ip']

### Multi-Threading
          
    th = threading.Thread(target=monitor_ip_job, args=(incoming_msg,))
    threads.append(th)  # appending the thread to the list
    # starting the threads
    for th in threads:
        th.start()
    # waiting for the threads to finish
    for th in threads:
        th.join()
        
>Threading was used to all multiple functions to be ran at once and allow for reaccuring monitoring of desired interfaces and devices

## TO-DO
1. Install the files found inside the Network_Monitoring folder\

2. Go into the `381Bot.py` file and change the: Teams_Token, Bot_Email & Bot_URL to match that of you webex bot

<img src='images/bot.png' width=100% />


You can get your bot_url by going into your terminal and entering the command:
          
          ngrok http 5001
