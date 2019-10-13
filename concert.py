import json
import datetime
import requests
import sys
from currency import getRate
from places import get_lat_lng_pair

baseURI = 'https://app.ticketmaster.com'
api_key = open('api_keys.txt').read().split("\n")[2]

def getEvents(artist):
    URI = baseURI + "/discovery/v2/events?apikey=%s&keyword=%s&locale=*&size=200" % (api_key, artist)
    response = requests.get(URI) 
    try:
        events = json.loads(response.content)['_embedded']['events']
        return events
    except:
        return []


def getCity(event):
    try:
        return event['_embedded']['venues'][0]['city']['name']
    except:
        return ""

def getVenueName(event):
    try:
        return event['_embedded']['venues'][0]['name']
    except:
        return ""

def getPC(event):
    try:
        return event['_embedded']['venues'][0]['postalCode']
    except:
        return ""

def getAddress(event):
    try:
        address = ''.join(event['_embedded']['venues'][0]['address'].values())
        return address
    except:
        return ""

def getLongitude(event):
    try:
        return event['_embedded']['venues'][0]['location']['longitude']
    except:
        return ""

def getLatitude(event):
    try:
        return event['_embedded']['venues'][0]['location']['latitude']
    except:
        return ""

def getDate(event):
    try:
        return event['dates']['start']['localDate']
    except:
        return ""

def getTime(event):
    try:
        if 'localTime' not in event['dates']['start']:
            return "00:00:00"
        return event['dates']['start']['localTime']
    except:
        return ""

def getCurency(event):
    try:
        return event['priceRanges'][0]['currency']
    except:
        return ""

def getPrice(event):
    if 'priceRanges' not in event:
        return []
    ps = event['priceRanges']
    if ps != [] :
        minPrice = ps[0]['min']
        for p in ps:
            if p['min'] < minPrice:
                minPrice = p['min']
        currency = getCurency(event)
        if currency != 'EUR':
            rate = getRate(currency)
            return int(float(minPrice*rate)*100)
        else:
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
    try:
        url = event['url']
        return url
    except:
        return ""

def getName(event):
    try:
        return event['name']
    except:
        return ""

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
        "longitude": getLongitude(event),
        "latitude": getLatitude(event) 
    }
    if result["longitude"] == "" or result["latitude"] == "":
        query_string = "%s %s %s %s" % (result["name"], result["address"], result["postcode"], result["city"])
        lat_lng_pair = get_lat_lng_pair(query_string)            
        result["latitude"] = str(lat_lng_pair[0])
        result["longitude"] = str(lat_lng_pair[1])
    return result

def getKeywordEvents(keyword):
    events = getEvents(keyword)
    result = []
    for event in events:
        temp = {}
        try:
            temp['event'] = getEventJson(event)
            temp['venue'] = getVenueJson(event)
        except KeyError:
            break
        #### uncomment to skip things without price info
        #if temp['event']["price_pp"] != []:
        #    result.append(temp)
        result.append(temp)
    return result


if __name__ == "__main__":
    print(getKeywordEvents(sys.argv[1]))