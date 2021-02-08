from scapy.layers.l2 import ARP, Ether, srp

class NodeLANScan(object):

    def __init__(self):
        self.hostList = []

    def LANScan(self, nodeIP):

        #Creates ARP Packet
        arpPacket = ARP(pdst=nodeIP+"/24")

        #Creates Ether Broadcast Packet
        etherPacket = Ether(dst="ff:ff:ff:ff:ff:ff")

        #Stacking etherPacket and arpPacket
        fullPacket = etherPacket / arpPacket

        result = srp(fullPacket, timeout=3, verbose=0)[0]

        for sent, received in result:
            self.hostList.append("IP Address: "+received.psrc+"\tMAC Address: "+ received.hwsrc)

        for hosts in self.hostList:
            print(hosts)

if __name__ == "__main__":
    node = NodeLANScan()