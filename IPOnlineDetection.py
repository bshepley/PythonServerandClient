import os

#This program answers the first one-to-one job
class IPOnlineDetection(object):

    def __init__(self):
        self.output = ""

    def detectIPStatus(self, targetIP):

        rep = os.system('ping ' + targetIP)

        if rep == 0:
            self.output = "Target IP: "+targetIP + " Online"
        else:
            self.output = "Target IP: "+targetIP + " Offline"