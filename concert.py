import ticketpy
import json

api_key = open('tm_key.txt').read()
tm_client = ticketpy.ApiClient(api_key)

def getEvents(artist):

    events = tm_client.events.find(keyword=artist).all()
        # City, address, venue, ppostcode, longitude, latitude, Date, Time, Price, Accessibility

    return events

def getCity(event):
    print(event.venues[0].city)
    return event.venues[0].city

def getVenueName(event):
    return event.venues[0].name

def getPC(event):
    return event.venues[0].postal_code

def getAddress(event):
    return event.venues[0].address 

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

    
test = getEvents('Hozier')

for t in test:

    if(getPrice(t) != []):
        print("City: " + getCity(t) + "\n")
        print("Venue: " + getVenueName(t) + "\n")
        print("Address: " + getAddress(t) + "\n")
        print("Postcode: " + getPC(t) + "\n")
        print("Date: " + getDate(t) + "\n")
        print("Time: " + getTime(t) + "\n")
        print("Price: " + getPrice(t) + "\n")
        print("____________________")
    else:
        print("Concert Sold Out")
    
