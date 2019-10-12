import ticketpy
import json
import datetime
import requests

baseURI = 'https://app.ticketmaster.com'
api_key = open('tm_key.txt').read()
tm_client = ticketpy.ApiClient(api_key)

def getEvents(artist):

    URI = baseURI + "/discovery/v2/events?keyword=%s&apikey=%s" % (artist, api_key)
    response = requests.get(URI) 
    events = json.loads(response.content)['_embedded']['events']

    #events = tm_client.events.find(keyword=artist).all()
        # City, address, venue, postcode, longitude, latitude, Date, Time, Price, Accessibility
    return events

def getCity(event):
    return event['_embedded']['venues'][0]['city']['name']

def getVenueName(event):
    return event['_embedded']['venues'][0]['name']

def getPC(event):
    return event['_embedded']['venues'][0]['postalCode']

def getAddress(event):
    address = ''.join(event['_embedded']['venues'][0]['address'].values())
    return address

def getLongitude(event):
    return event['_embedded']['venues'][0]['location']['longitude']

def getLatitude(event):
    return event['_embedded']['venues'][0]['location']['latitude']

def getDate(event):
    return event['dates']['start']['localDate']
def getTime(event):
    if 'localTime' not in event['dates']['start']:
        return "00:00:00"
    return event['dates']['start']['localTime']

def getPrice(event):
    if 'priceRanges' not in event:
        return []
    ps = event['priceRanges']
    if ps != [] :
        minPrice = ps[0]['min']
        for p in ps:
            if p['min'] < minPrice:
                minPrice = p['min'] 
        return int(float(minPrice)*100)
    else :
        return ps

def concertSoldOut(event):
    if(getPrice(event) == []):
        return True
    else:
        return False

# no API call to get URL, do this the old fashioned way
def getURL(event):
    url = event['url']
    return url

def getName(event):
    return event['name']

def getEventJson(event):
    time = datetime.datetime.strptime(getDate(event)+" "+getTime(event), "%Y-%m-%d %H:%M:%S").timestamp()
    result = {
        "name": getName(event),
        "start": time,
        "url": getURL(event),
        "price_pp": getPrice(event)
    }
    return result

def getVenueJson(event):
    result = {
        "name": getVenueName(event),
        "address": getAddress(event),
        "postcode": getPC(event),
        "city": getCity(event),
        "longtitude": getLongitude(event),
        "latitude": getLatitude(event) 
    }
    return result


############### TEST ################
    
test = getEvents('Aerosmith')

result = []

for t in test:
    temp = {}
    temp['event'] = getEventJson(t)
    temp['venue'] = getVenueJson(t)
    if temp['event']["price_pp"] != []:
        result.append(temp)
    # if not concertSoldOut(t):
    #     print("Name: " + getName(t) + '\n')
    #     print("City: " + getCity(t) + "\n")
    #     print("Venue: " + getVenueName(t) + "\n")
    #     print("Address: " + getAddress(t) + "\n")
    #     print("Postcode: " + getPC(t) + "\n")
    #     print("Longitude: " + getLongitude(t) + "\n")
    #     print("Latitude: " + getLatitude(t) + "\n")
    #     print("Date: " + getDate(t) + "\n")
    #     print("Time: " + getTime(t) + "\n")
    #     print("Price: " + getPrice(t) + "\n")
    #     print(getURL(t) + "\n")
    #     print("____________________")
    # else:
    #     print("Concert Sold Out")
    #     print("____________________")
    
print(json.dumps(result))