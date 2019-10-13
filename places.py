import requests
import json

api_key = open('api_keys.txt').read().split("\n")[3]
baseURI = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&inputtype=textquery&key=%s&fields=geometry'

def get_lat_lng_pair(string):
    response = requests.get(baseURI % (string, api_key))
    data = json.loads(response.content)
    if data["status"] == "OK":
        location = data["candidates"][0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
        return (lat,lng)
    raise KeyError

if __name__ == "__main__":
    print(get_lat_lng_pair("MIND Milano Innovation District (Area Expo) 20017 Milano"))

