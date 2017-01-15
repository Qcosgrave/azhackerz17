from amadeus import Flights
import json
import datetime

def find_flight(orig, dest, event_date):
    flights = Flights('c6V1ViNs78CkiATUMajLlVaOImNAdDa4')

    # Convert to datetime object
    event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S').date()

    depart_high = event_date - datetime.timedelta(days=1)
    depart_low = event_date - datetime.timedelta(days=3)

    departure_string = str(depart_low) + "--" + str(depart_high)

    resp = flights.extensive_search(
        origin=orig,
        destination=dest,
        departure_date=departure_string,
        duration='4--7',
        max_price=3000)

    # print json.dumps(resp, indent=2, sort_keys=True)
    # currency = resp['currency']

    for flight in resp.get('results', [])[:5]:
        airline = flight['airline']
        departure_date = datetime.datetime.strptime(flight['departure_date'], '%Y-%m-%d')
        return_date = datetime.datetime.strptime(flight['return_date'], '%Y-%m-%d')
        price = flight['price']

        url_string = "https://www.google.com/flights/#search;f=%s;t=%s;d=%s;r=%s;a=%s" % (orig, dest, str(departure_date.date()), str(return_date.date()), airline)
        print url_string

        print "For %s you can fly to %s departing on %s and returning on %s" % (price, dest, departure_date.strftime('%b %d, %Y'), return_date.strftime('%b %d, %Y'))
