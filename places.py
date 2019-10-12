import requests
import json

api_key = open('places_key.txt').read()
baseURI = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&inputtype=textquery&key=%s&fields=geometry'

def get_lat_lng_pair(string):
    response = requests.get(baseURI % (string, api_key))
    data = json.loads(response.content)
    if data["status"] == "OK":
        location = data["candidates"][0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
        return (lat,lng)

if __name__ == "__main__":
    print(get_lat_lng_pair("MIND Milano Innovation District (Area Expo) 20017 Milano"))

