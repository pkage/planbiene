import json
import asyncio
import requests
import timeit

from dateutil import parser
from datetime import datetime
from datetime import timedelta
import time

import concert 
import airports as ap 



keys = open('api_keys.txt').read().split("\n")
SKY_API_KEY = keys[0]
GEO_API_KEY = keys[1]
URI = "https://www.skyscanner.net/g/chiron"


# access root of request, get client data
# replace this with actual ip
IP = "147.83.201.97"


# hardcoded for now
LOCALE_CODE = "en-GG"
CURRENCY_CODE = "EUR"




def getuserdata(ip):
    try:
        resp = requests.get("http://api.ipstack.com/"+ip+"?access_key="+GEO_API_KEY).json()
        return resp["country_code"], resp["country_name"], resp["city"], float(resp["latitude"]), float(resp["longitude"])
    except:
        return "ES", "Spain", "Barcelona",  41.394378662109375, 2.1131200790405273



COUNTRY_CODE, COUNTRY_NAME, CITY, LAT, LON = getuserdata(IP)

# gets cheapest flights based on the parameters given
def get_flight(from_city, to_city, from_date, to_date, country, currency, locale):
    print(URI + "/api/v1/flights/browse/browsequotes/v1.0/" 
        + country + "/"
        + currency + "/"
        + locale + "/"
        + from_city + "/"
        + to_city + "/"
        + from_date + "/"
        + to_date)
    response = requests.get(URI + "/api/v1/flights/browse/browsequotes/v1.0/" 
        + country + "/"
        + currency + "/"
        + locale + "/"
        + from_city + "/"
        + to_city + "/"
        + from_date + "/"
        + to_date,
        headers={
            "api-key" : SKY_API_KEY,
            "Accept" : "application/json"
        }
        ).json()

    return response


# get locales supported by skyscanner
def get_locales():
    return requests.get(URI + "/api/v1/localisation/reference/v1.0/locales",
        headers={
            "api-key" : SKY_API_KEY,
            "Accept" : "application/json"
        }).json()

# get countries supported by skyscanner and format them in a dictionary accessible by country name
def get_country(locale):
    
    resp = requests.get(URI + "/api/v1/localisation/reference/v1.0/countries/" + locale,
        headers={
            "api-key" : SKY_API_KEY,
            "Accept" : "application/json"
        }).json()

    res = {}
    for e in resp["Countries"]:
        res[e["Name"]] = e["Code"]
    
    return res

# get currencies
async def get_currencies(): 

    """
    {
            "Code": "EUR",
            "Symbol": "€",
            "ThousandsSeparator": ".",
            "DecimalSeparator": ",",
            "SymbolOnLeft": false,
            "SpaceBetweenAmountAndSymbol": true,
            "RoundingCoefficient": 0,
            "DecimalDigits": 2
    }
    """
    
    return requests.get(URI + "/api/v1/localisation/reference/v1.0/currencies",
        headers = {
            "api-key" : SKY_API_KEY
        }).json()

# get an autocompleted place from parameters and a query.
def get_places(country, currency, locale, query):

    return requests.get(URI + "/api/v1/places/autosuggest/v1.0/"
        + country + "/"
        + currency + "/" 
        + locale 
        + "?query=" + query,
        headers={
            "api-key" : SKY_API_KEY

        } ).json()["Places"]

# put all that shit together and just get some flights for a specified date.
async def get_cheapest_quotes(start, end, when="anytime", direct=False):


    # TODO: add direct filter

    country = get_country(LOCALE_CODE)[COUNTRY_NAME]
    
    _start = get_places(country, CURRENCY_CODE, LOCALE_CODE, start)
    _start = _start[0]["PlaceId"]
    _end =   get_places(country, CURRENCY_CODE, LOCALE_CODE, end)
    _end = _end[0]["PlaceId"]
    #print(_start)
    #print(_end)

    flights = get_flight(from_city=_start, 
                         to_city=_end, 
                         from_date=when,
                         to_date="",
                         country=country,
                         currency=CURRENCY_CODE,
                         locale=LOCALE_CODE)

    return flights

async def get_session(country, from_place, to_place, leave_date, 
                passenger_no, carriers):


    # print(country)
    # print(CURRENCY_CODE)
    # print(LOCALE_CODE)
    # print(from_place)
    # print(to_place)
    # print(leave_date)
    # print(passenger_no)
    # print(carriers)
    # "inboundDate" : return_date,
    return requests.post(URI + "/api/v1/flights/search/pricing/v1.0",
        headers={
            "api-key" : SKY_API_KEY,
            "Content-Type" : "application/x-www-form-urlencoded",
            "X-Forwarded-For" : IP,
            "Accept" : "application/json"
        },
        data=json.dumps({
            "country" : country,
            "currency" : CURRENCY_CODE,
            "locale" : LOCALE_CODE,
            "originPlace" : from_place,
            "destinationPlace" : to_place,
            "outboundDate" : leave_date.split("T")[0],
            "adults" : passenger_no,
            "includeCarriers" : carriers
        })).json()

async def poll_results():

    return requests.get(URI + "/api/v1/flights/search/pricing/v1.0") 


async def bookings(session_id):

    return requests.get(URI 
        + "/api/v1/flights/search/pricing/v1.0?session_id=" 
        + session_id 
        + "&sortType=price&sortOrder=desc&stops=0",
        headers={
            "api-key" : SKY_API_KEY,
            "Accept" : "application/json"
        }
        ).json()


async def filter_bookings(bookings, max_price=5000, max_time=3700, max_stops=5):
    
    itineraries = bookings["Itineraries"]#[0:1000]
    legs        = bookings["Legs"]
    segments    = bookings["Segments"]
    carriers    = bookings["Carriers"]
    places      = bookings["Places"]

    possible_itins = {}
    leg_ids = []

    _places = {}
    _carriers = {}
    for place in places:
        _places[place["Id"]] = {
            "code" : place["Code"],
            "name" : place["Name"]
        }

    for carrier in carriers:
        _carriers[carrier["Id"]] = carrier["DisplayCode"]

    for itin in itineraries:
        prices = itin["PricingOptions"]
        for price in prices:
            if price["Price"] <= max_price:
                possible_itins[itin["OutboundLegId"]] = {
                    "price": price["Price"],
                    "uri" : price["DeeplinkUrl"]
                }
                leg_ids.append(itin["OutboundLegId"])

    for leg in legs:
        if leg["Id"] in leg_ids:
            if (len(leg["Stops"]) <= max_stops) and (int(leg["Duration"]) <= max_time):
                possible_itins[leg["Id"]]["duration"] = leg["Duration"]
                possible_itins[leg["Id"]]["departure"] = leg["Departure"]
                possible_itins[leg["Id"]]["arrival"] = leg["Arrival"]
                possible_itins[leg["Id"]]["airports"] = [ leg["OriginStation"] ] + leg["Stops"] + [ leg["DestinationStation"] ]
                possible_itins[leg["Id"]]["airports"] = map(lambda x: _places[x] 
                                                            ,possible_itins[leg["Id"]]["airports"])
                possible_itins[leg["Id"]]["numbers"] = []
                for fn in leg["FlightNumbers"]:
                    possible_itins[leg["Id"]]["numbers"].append(
                                            _carriers[fn["CarrierId"]]
                                            + str(fn["FlightNumber"]))

    return possible_itins


async def get_bookings(start, country, end, direct=False, when="anytime", passenger_no=1, way="undef"):

    _start = get_places(country, CURRENCY_CODE, LOCALE_CODE, start)
    _start = _start[0]["PlaceId"]
    _end = get_places(country, CURRENCY_CODE, LOCALE_CODE, end)
    _end = _end[0]["PlaceId"]

    quotes = get_flight(from_city=_start, 
                         to_city=_end, 
                         from_date=when,
                         to_date="",
                         country=country,
                         currency=CURRENCY_CODE,
                         locale=LOCALE_CODE)

    # {'QuoteId': 1, 'MinPrice': 78.0, 'Direct': False, 
    # 'OutboundLeg': {'CarrierIds': [1878], 
    #                 'OriginId': 89023, 
    #                 'DestinationId': 54353, 
    #                 'DepartureDate': '2019-10-22T00:00:00'}, 
    # 'QuoteDateTime': '2019-10-08T12:08:00'}

    carrier_ids = []
    #for carrier in quotes["Carriers"]:
    #    carrier_ids.append(str(carrier["CarrierId"]))
    
    try:
        quotes = quotes["Quotes"]
    except KeyError:
        quotes = []
    minPrice = 1000000
    for quote in quotes:
        if (quote["MinPrice"] < minPrice 
            and parser.parse(quote["OutboundLeg"]["DepartureDate"]) > datetime.now() ):
            carrier_ids = map(str, quote["OutboundLeg"]["CarrierIds"])
            when = quote["OutboundLeg"]["DepartureDate"]


    print(carrier_ids)
    
    session_id = await get_session(country, _start, _end, 
                             when, passenger_no, 
                             ",".join(carrier_ids))

    
    try:
        print(session_id)
        session_id = session_id["session_id"]
    except:
        print(session_id)
        return {way : []}

    _bookings = await bookings(session_id) 
    filtered = await filter_bookings(_bookings)

    _filtered = []
    for f in filtered:
        try:
            _filtered.append({
                "numbers" : filtered[f]["numbers"],
                "airports" : filtered[f]["airports"],
                "departure_time" : filtered[f]["departure"],
                "arrival_time" : filtered[f]["arrival"],
                "price" : int(float(filtered[f]["price"])*100),
                "duration" : filtered[f]["duration"],
                "uri" : filtered[f]["uri"]
            })
        except KeyError:
            pass

    _filtered.sort(key=lambda x: x["price"], reverse=False)

    """
    for f in _filtered:
        try:
            del f["uri"]
            print(f)
            print("- - - -")
        except KeyError:
            pass 
    """
    try:
        return {way : _filtered[0]}
    except:
        return {way : _filtered}


async def get_bookings_both_ways(start, end, direct=False, when="anytime", passenger_no=1): 


    one_way = asyncio.ensure_future(get_bookings(start, end, direct, when, passenger_no))
    
    try: 
        timestamp = time.mktime(datetime.strptime(when, "%Y-%m-%d").timetuple()) + timedelta(days=1).total_seconds()
    except ValueError:
        timestamp = time.mktime(datetime.strptime(when, "%Y-%m").timetuple()) + timedelta(days=1).total_seconds()
    try:
        when = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    except ValueError:
        when = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m')

    other_way = asyncio.ensure_future(get_bookings(end, start, direct, when, passenger_no))


    loop = asyncio.get_event_loop()
    bothways = asyncio.gather(one_way, other_way)
    results = loop.run_until_complete(bothways)

    #print(results)

    price1 = 0
    price2 = 0
    try:
        price1 = one_way[0]["price"]
    except:
        pass

    try:
        price2 = other_way[0]["price"]
    except:
        pass


    """
    return {
        "price_pp": price1 + price2,
        "outbound" : one_way[0],
        "return" : other_way[0]
    }"""
    return results


def get_all_the_events_boy(start, destinations, direct,passenger_no):
    
    """
    destinations = [ 
        {
            "end" : "airport1"
            "date" : 2011
        },
        ...
    ]
    """


    country = get_country(LOCALE_CODE)[COUNTRY_NAME]


    tasks = []
    for dest in destinations:
        when = dest["date"]
                                    # start, _start, country, end, direct=False, when="anytime", passenger_no=1, way="undef"
        one_way = asyncio.ensure_future(get_bookings(start=start, 
                                                    country=country, 
                                                    end=dest["end"], 
                                                    direct=direct, 
                                                    when=when, 
                                                    passenger_no=passenger_no, 
                                                    way="forward"))
    
        try: 
            timestamp = time.mktime(datetime.strptime(when, "%Y-%m-%d").timetuple()) + timedelta(days=1).total_seconds()
        except ValueError:
            timestamp = time.mktime(datetime.strptime(when, "%Y-%m").timetuple()) + timedelta(days=1).total_seconds()
        try:
            when = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        except ValueError:
            when = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m')
                                                    # start, _start, country, end, direct=False, when="anytime", passenger_no=1, way="undef"
        other_way = asyncio.ensure_future(get_bookings(start=dest["end"],
                                                       country=country, 
                                                       end=start, 
                                                       direct=direct, 
                                                       when=when, 
                                                       passenger_no=passenger_no, 
                                                       way="back"))

        tasks.append(one_way)
        tasks.append(other_way)

    loop = asyncio.get_event_loop()
    bothways = asyncio.gather(*tasks)

    results = loop.run_until_complete(bothways)
    return results


def get_gigs(home, keyword, direct=False, passenger_no=1):
    gigs = concert.getKeywordEvents(keyword)

    destinations = []
    for gig in gigs:
        date = datetime.utcfromtimestamp(gig["event"]["start"]).strftime('%Y-%m-%d') 
        lat = gig["venue"]["latitude"]
        log = gig["venue"]["longitude"]
        airport = ap.closest_airport(lat, log, 1)
        destinations.append({
            "date" : date,
            "end" :  airport[0]
        })

    res = get_all_the_events_boy(home, destinations, direct=False, passenger_no=passenger_no)


    _gigs = []
    
    for i in range(0, len(gigs)):
        _gig = gigs[i]

        outbound = res.pop(0)
        backhome = res.pop(0)

        _gig["flights"] = {
            "outbound" : outbound,
            "return"   : backhome
        }

        _gigs.append(_gig)
    return _gigs



start = timeit.default_timer()
    


print(get_gigs("DUB", "Hozier"))

#get_all_the_events_boy(start="Vilnius",  
#                       destinations=[], direct=False, passenger_no=1)
stop = timeit.default_timer()
print('Time: ', stop - start)  
# EXAMPLE USAGE:
# get_bookings(start="Vilnius", end="Edinburgh", direct=False, when="2020-01", passenger_no=1)
# MANDATORY FIELDS:
# start - location to fly from
# end - location to fly to
# OPTIONAL FIELDS:
# direct - direct flights only. defaults to False
# when - day or month in which the flight should take place. defaults to anytime
# passenger_no - number of passengers for the flight. defaults to 1

"""
[
                           {
                               "end" : "BCN",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "BCN",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "BCN",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "KUN",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "RIX",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "GLA",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "YVR",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "ADA",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "LGW",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "LHR",
                               "date" : "2020-01-06"
                           },
                           {
                               "end" : "IAD",
                               "date" : "2020-01-06"
                           },
                       ]
"""                       
