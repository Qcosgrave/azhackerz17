import eventful
import json
import find_airport
import find_flight

def find_events(artist):
    print "Search for " + artist

    api = eventful.API('JB3k5tX9CDjWhC3m')

    performers = api.call('/performers/search', keywords=artist)

    if int(float(performers['page_count'])) == 0:
        print "No artist found"
        quit()

    dict_or_list = performers['performers']['performer']

    if type(dict_or_list) is dict:
        performer_id = performers['performers']['performer']['id']
        event_count = performers['performers']['performer']['event_count']
    else:
        performer_id = performers['performers']['performer'][0]['id']
        event_count = performers['performers']['performer'][0]['event_count']

    event_count = int(float(event_count))

    if event_count != 0:
        events = api.call('/performers/events/list', id=performer_id)['event']
        print json.dumps(events, indent=2, sort_keys=True)

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

            dest_airport_code = find_airport.find_airport(longitude, latitude)

            find_flight.find_flight("FRA", dest_airport_code, start_time)

            # print "Located in %s, %s, %s. %s." % (city, region, country, event_title)
    else:
        print "No events for " + artist
