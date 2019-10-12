import json
import requests

keys = open('api_keys.txt').read().split("\n")
SKY_API_KEY = keys[0]
GEO_API_KEY = keys[1]
URI = "https://www.skyscanner.net/g/chiron"


# access root of request, get client data
# replace this with actual ip
ip = "147.83.201.97"


# hardcoded for now
LOCALE_CODE = "en-GG"
CURRENCY_CODE = "EUR"




def getuserdata(ip):
    try:
        resp = requests.get("http://api.ipstack.com/"+ip+"?access_key="+GEO_API_KEY).json()
        return resp["country_code"], resp["country_name"], resp["city"], float(resp["latitude"]), float(resp["longitude"])
    except:
        return "ES", "Spain", "Barcelona",  41.394378662109375, 2.1131200790405273



COUNTRY_CODE, COUNTRY_NAME, CITY, LAT, LON = getuserdata(ip)

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
                         from_date="anytime",
                         to_date="",
                         country=country,
                         currency=CURRENCY_CODE,
                         locale=LOCALE_CODE)

    return flights

                        
def get_bookings():
    return False


flights = get_cheapest_quotes("Vilnius", "Glasgow")
print(flights["Quotes"][0])
print(flights["Places"])
print(flights["Carriers"])
print(flights["Currencies"])