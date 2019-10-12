import ticketpy
import json

api_key = open('tm_key.txt').read()
tm_client = ticketpy.ApiClient(api_key)

def getEvents(artist):

    events = tm_client.events.find(keyword=artist).all()
        # City, address, venue, postcode, longitude, latitude, Date, Time, Price, Accessibility

    return events

def getCity(event):
    return event.venues[0].city

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
    return event.local_start_date
def getTime(event):
    return event.local_start_time

def getPrice(event):

    ps = event.price_ranges

    if ps != [] :

        minPrice = ps[0]["min"]

        for p in ps:
            if p["min"] < minPrice:
                minPrice = p["min"] 

        return str (minPrice)

    else :
        return ps

def concertSoldOut(event):
    if(getPrice(event) == []):
        return True
    else:
        return False

def getURL(event):
    result = "URL: ".join(event.links)
    return result



############### TEST ################
    
test = getEvents('Hozier')

for t in test:

    if not concertSoldOut(t):
        print("City: " + getCity(t) + "\n")
        print("Venue: " + getVenueName(t) + "\n")
        print("Address: " + getAddress(t) + "\n")
        print("Postcode: " + getPC(t) + "\n")
        print("Longitude: " + getLongitude(t) + "\n")
        print("Latitude: " + getLatitude(t) + "\n")
        print("Date: " + getDate(t) + "\n")
        print("Time: " + getTime(t) + "\n")
        print("Price: " + getPrice(t) + "\n")
        print(getURL(t) + "\n")
        print("____________________")
    else:
        print("Concert Sold Out")
        print("____________________")
    
