# This is an object of point object to store the latitude and longitude of a point
# Just simple getter to get the values
class Point:
    latitude = 0
    longitude = 0
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    def getLatitude(self):
        return self.latitude
    def getLongitude(self):
        return self.longitude