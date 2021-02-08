import socket

class SpecificPortDetection(object):

    def __init__(self):
        self.output = ""

    def checkPort(self, targetIP, targetPort):
        checkerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        targetLocation = (targetIP, targetPort)
        portStatus = checkerSocket.connect_ex(targetLocation)

        if portStatus == 0:
            self.output = "Target IP Address: "+targetIP +" Target Port: "+ str(targetPort) +": "+ " Open"
        else:
            self.output = "Target IP Address: "+targetIP +" Target Port: "+ str(targetPort) +": "+ " Closed"

        checkerSocket.close()