import urllib2
import os
import json
import sys
import eventful
import datetime
from amadeus import Flights
import spotipy
import spotipy.util as util

amideus_api = 'c6V1ViNs78CkiATUMajLlVaOImNAdDa4'
# find_airport
# This function finds the most relevant airport nearby given longitude/latitude coordinates
# Uses Amadeus API (https://sandbox.amadeus.com/getting-started)
def find_airport(longitude, latitude):
    airport_content = urllib2.urlopen("https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?apikey=" + amideus_api + "&latitude=" + latitude + "&longitude=" + longitude).read()
    airport_content = json.loads(airport_content)
    return airport_content[0]['airport']

# find_flight
# This function will find flights based off origin, destination, and an event date to center around
# Uses Amadeus API (https://sandbox.amadeus.com/getting-started)
def find_flight(orig, dest, event_date):
    flights = Flights(amideus_api)

    # Convert to datetime object
    event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S').date()

    # Decrememnt date to get departures before the event
    depart_high = event_date - datetime.timedelta(days=1)
    depart_low = event_date - datetime.timedelta(days=3)

    # String for range of dates
    departure_string = str(depart_low) + "--" + str(depart_high)

    # The request :)
    resp = flights.extensive_search(
        origin=orig,
        destination=dest,
        departure_date=departure_string,
        duration='4--7',
        max_price=3000)

    # print json.dumps(resp, indent=2, sort_keys=True)
    # currency = resp['currency']

    # Loop through each found flight and print its info
    for flight in resp.get('results', [])[:5]:
        airline = flight['airline']
        departure_date = datetime.datetime.strptime(flight['departure_date'], '%Y-%m-%d')
        return_date = datetime.datetime.strptime(flight['return_date'], '%Y-%m-%d')
        price = flight['price']

        # Create a URL to find these flights on google
        url_string = "https://www.google.com/flights/#search;f=%s;t=%s;d=%s;r=%s;a=%s" % (orig, dest, str(departure_date.date()), str(return_date.date()), airline)

        print "For %s you can fly to %s departing on %s and returning on %s" % (price, dest, departure_date.strftime('%b %d, %Y'), return_date.strftime('%b %d, %Y'))


# find_events
# This function will find events that a specified artist is performing at
# Uses Eventful API (http://api.eventful.com/)
def find_events(artist):
    print "Search for " + artist

    api = eventful.API('JB3k5tX9CDjWhC3m')

    performers = api.call('/performers/search', keywords=artist)

    if int(float(performers['page_count'])) == 0:
        print "No artist found"
        quit()

    dict_or_list = performers['performers']['performer']

    # Get performer info. Must check if it is a list or a dict because sometimes there are multiple
    # performers going by same or similar names
    if type(dict_or_list) is dict:
        performer_id = performers['performers']['performer']['id']
        event_count = performers['performers']['performer']['event_count']
    else:
        performer_id = performers['performers']['performer'][0]['id']
        event_count = performers['performers']['performer'][0]['event_count']

    # Don't bother if the artist has no events :^)
    event_count = int(float(event_count))
    if event_count != 0:
        events = api.call('/performers/events/list', id=performer_id)['event']
        # print json.dumps(events, indent=2, sort_keys=True)

        # Loop through each event, printing its info and finding flights
        for event in events:
            city = event['city']
            region = event['region']
            country = event['country']
            start_time = event['start_time']
            event_title = event['title']
            url = event['url']
            event_id = event['id']

            event_info = api.call('events/get', id=event_id)
            longitude = event_info['longitude']
            latitude = event_info['latitude']

            dest_airport_code = find_airport(longitude, latitude)

            find_flight("TUS", dest_airport_code, start_time)

            print "Located in %s, %s, %s. %s." % (city, region, country, event_title)
    else:
        print "No events for " + artist

### Spotify ###
scope = 'user-follow-read user-top-read'
username = 'calvinm13'
token = util.prompt_for_user_token(username, scope, '8e5cac0ed299444480f463d1a662829f', '078527b8e4394a1c8efd5c07bce12568', 'http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)
    followed_results = sp.current_user_followed_artists()
    top_results = sp.current_user_top_artists()
    # print json.dumps(results, indent=2, sort_keys=True)
else:
    print "Can't get token for", username

# Initialize artists list
artists = []

# Create simple list of artists from top artists and followed artists
for item in followed_results['artists']['items']:
    artists.append(item['name'])
for item in top_results['items']:
    artists.append(item['name'])

# Find artist events
for item in artists:
    find_events(item)
