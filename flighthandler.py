import json
import requests

from dateutil import parser
from datetime import datetime

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
def get_currencies(): 

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
def get_cheapest_quotes(start, end, when="anytime", direct=False):


    # TODO: add direct filter

    country = get_country(LOCALE_CODE)[COUNTRY_NAME]
    
    _start = get_places(country, CURRENCY_CODE, LOCALE_CODE, start)[0]["PlaceId"]
    _end =   get_places(country, CURRENCY_CODE, LOCALE_CODE, end)[0]["PlaceId"]
    print(_start)
    print(_end)

    flights = get_flight(from_city=_start, 
                         to_city=_end, 
                         from_date=when,
                         to_date="",
                         country=country,
                         currency=CURRENCY_CODE,
                         locale=LOCALE_CODE)

    return flights

def get_session(country, from_place, to_place, leave_date, 
                passenger_no, carriers):


    print(country)
    print(CURRENCY_CODE)
    print(LOCALE_CODE)
    print(from_place)
    print(to_place)
    print(leave_date)
    print(passenger_no)
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


def poll_results():

    return requests.get(URI + "/api/v1/flights/search/pricing/v1.0") 


def get_bookings(start, end, direct=False, when="anytime", passenger_no=1):

    country = get_country(LOCALE_CODE)[COUNTRY_NAME]

    _start = get_places(country, CURRENCY_CODE, LOCALE_CODE, start)[0]["PlaceId"]
    _end =   get_places(country, CURRENCY_CODE, LOCALE_CODE, end)[0]["PlaceId"]

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

    quotes = quotes["Quotes"]
    minPrice = 1000000
    for quote in quotes:
        if (quote["MinPrice"] < minPrice 
            and parser.parse(quote["OutboundLeg"]["DepartureDate"]) > datetime.now() ):
            carrier_ids = map(str, quote["OutboundLeg"]["CarrierIds"])
            when = quote["OutboundLeg"]["DepartureDate"]


    print(carrier_ids)

    session_id = get_session(country, _start, _end, 
                             when, passenger_no, 
                             ",".join(carrier_ids))

    session_id = session_id["session_id"]
    print("SESSION ID: ")
    print(session_id)

    print(bookings(session_id)["Itineraries"][0:10][0])
    for el in bookings(session_id)["Itineraries"][0:30]:
        for prices in el["PricingOptions"]:
            print (prices["Price"])
        print("-------")

def bookings(session_id):

    return requests.get(URI 
        + "/api/v1/flights/search/pricing/v1.0?session_id=" 
        + session_id,
        headers={
            "api-key" : SKY_API_KEY,
            "Accept" : "application/json"
        },
        data=json.dumps({
            "sortType" : "price",
            "sortOrder" : "desc",
            "stops" : 1
        })).json()
    



    


get_bookings("Vilnius", "Edinburgh", "2019-12")

