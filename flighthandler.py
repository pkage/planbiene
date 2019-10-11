import json
import requests


API_KEY = open('api_keys.txt').read()
URI = "https://www.skyscanner.net/g/chiron/"




def get_flight(from_city, to_city, date):
    response = requests.get(URI + "/flights/browse/browsequotes/v1.0/",
        params={
            "country" :  "",
            "currency" :"",
            "locale" :"",
            "originPlace" : "",
            "destinationPlace" : "",
            "outboundPartialDate" : "",
            "inboundPartialDate" :""
        })


def get_locales():
    return requests.get(URI + "/api/v1/localisation/reference/v1.0/locales",
        headers={
            "api-key" : API_KEY,
            "Accept" : "application/json"
        }).json()

def get_country(locale): 
    return requests.get(URI + "/reference/v1.0/countries/" + locale,
        headers={
            "Accept" : "application/json"
        }).json()

print(get_locales().json()[3])