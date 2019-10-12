import json
import requests


API_KEY = open('api_keys.txt').read()
URI = "https://www.skyscanner.net/g/chiron"




def get_flight(from_city, to_city, from_date, to_date, country, currency, locale):
    response = requests.get(URI + "/api/v1/flights/browse/browsequotes/v1.0/" 
        + country + "/"
        + currency + "/"
        + locale + "/"
        + from_city + "/"
        + to_city + "/"
        + from_date + "/"
        + to_date,
        headers={
            "api-key" : API_KEY,
            "Accept" : "application/json"
        }
        ).text

    return response



def get_locales():
    return requests.get(URI + "/api/v1/localisation/reference/v1.0/locales",
        headers={
            "api-key" : API_KEY,
            "Accept" : "application/json"
        }).json()

def get_country(locale):
    
    resp = requests.get(URI + "/api/v1/localisation/reference/v1.0/countries/" + locale,
        headers={
            "api-key" : API_KEY,
            "Accept" : "application/json"
        }).json()

    res = {}
    for e in resp["Countries"]:
        res[e["Name"]] = e["Code"]
    
    return res

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
            "api-key" : API_KEY
        }).json()


def get_places(country, currency, locale, query):

    return requests.get(URI + "/api/v1/places/autosuggest/v1.0/"
        + country + "/"
        + currency + "/" 
        + locale 
        + "?query=" + query,
        headers={
            "api-key" : API_KEY

        } ).json()["Places"]


    

locale = get_locales()["Locales"][2]["Code"]
country = get_country(locale)["United Kingdom"]
country2 = get_country(locale)["Lithuania"]
currency = "EUR"
query1 = "Vilnius"
query2 = "Glasgow"
place1 = get_places(country, currency, locale, query1)[0]["PlaceId"]
place2 = get_places(country, currency, locale, query2)[0]["PlaceId"]
print(place1)

flights = get_flight(from_city=country, 
                     to_city=country2, 
                     from_date="anytime",
                     to_date="",
                     country=country,
                     currency=currency,
                     locale=locale)

print(flights)