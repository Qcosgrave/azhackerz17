import urllib2
import os
import json
import sys

amideus_api = 'c6V1ViNs78CkiATUMajLlVaOImNAdDa4'

def find_airport(longitude, latitude):
    airport_content = urllib2.urlopen("https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?apikey=" + amideus_api + "&latitude=" + latitude + "&longitude=" + longitude).read()
    airport_content = json.loads(airport_content)
    return airport_content[0]['airport']
