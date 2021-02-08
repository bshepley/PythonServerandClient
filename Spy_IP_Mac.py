from scapy.layers.l2 import ARP, Ether, srp

'''
* NAME:
*TYPE: Return result.
*DESCRIPTION: The code allow the Job creator to spy on Job seeker's neighbours, the job creator could direct the job 
              seekers to report the IP address and MAC address for every live host who shares the same LAN with the job 
              seeker, the job creator should detect the job seekers that share the same LAN if any.
'''

target_ip = "192.168.0.1/24"
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether / arp

result = srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("-----------------------------------")
print("IP Address" + " " * 11 + "MAC Address")
print("-----------------------------------")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
