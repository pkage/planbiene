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
    events = json.loads(response.content)

    #events = tm_client.events.find(keyword=artist).all()
        # City, address, venue, postcode, longitude, latitude, Date, Time, Price, Accessibility

    return events

def getCity(event):
    return event['_embedded']['venues'][0]

def getVenueName(event):
    return event.venues[0].name

def getPC(event):
    return event.venues[0].postal_code

def getAddress(event):
    return event.venues[0].address 

def getLongitude(event):
    return event.venues[0].longitude

def getLatitude(event):
    return event.venues[0].latitude

def getDate(event):
    return event['dates']['start']['localDate']
def getTime(event):
    t = event['dates']['start']['localTime']
    time = t['hourOfDay'] + ":" + t['minuteOfHour']
    return time

def getPrice(event):

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
    event_json = event.links['self']
    baseURI = 'https://app.ticketmaster.com'
    URI = baseURI + event_json + '&apikey=' + api_key
    response = requests.get(URI)
    url = json.loads(response.content)['url']
    return url

def getName(event):
    return event.name

def getEventJson(event):
    time = datetime.datetime.strptime(getDate(event)+" "+getTime(event), "%Y-%m-%d %H:%M:%S").timestamp()
    result = json.dumps({
        "name": getName(event),
        "start": time,
        "url": getURL(event),
        "price_pp": getPrice(event)
    })
    print(result)
    return result


############### TEST ################
    
test = getEvents('Hozier')

for t in test:
    getEventJson(t)
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
    
