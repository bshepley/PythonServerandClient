from ip2geotools.databases.noncommercial import DbIpCity

class NodeLocation(object):

    def __init__(self):

        self.output = ""
        self.targetLat = 0
        self.targetLong = 0
        self.seekerLat = 0
        self.seekerLong = 0
        self.distance = 0

    def DistanceEquation(self, targetIP):

        targetLocation = DbIpCity.get(targetIP, api_key='free')
        self.targetLat = targetLocation.latitude
        self.targetLong = targetLocation.longitude

        seekerIP = input("Find your IP Address at 'https://www.whatismyip.com/' Then Enter That Address\n")

        seekerLocation = DbIpCity.get(seekerIP, api_key='free')
        self.seekerLat = seekerLocation.latitude
        self.seekerLong = seekerLocation.longitude

        distanceLat = (int(self.targetLat) - int(self.seekerLat))**2
        distanceLong = (int(self.targetLong) - int(self.seekerLong))**2
        self.distance = (int(distanceLat) + int(distanceLong))**0.5

        self.output = "Target IP: "+targetIP\
                      +" Latitude: "+str(self.targetLat) \
                      +" Longitude: "+str(self.targetLong)\
                      + " Distance: "+ str(self.distance)
