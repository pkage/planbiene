import mpu
import json
import sys
import numpy

airports_file = "airports.json"

def get_airports():
    with open(airports_file, "r") as content:
        return json.loads(content.read())

def distance(origin, destination):
    return mpu.haversine_distance(origin, destination)

# lat, lon: latitude/longtitude of the place to find an airport nearby
# num: number of airports nearby to fetch
# detailed: if True returns all data about airports, otherwise just the international code
def closest_airport(lat, lon, num, detailed = False):
    airports = get_airports()
    distances = []
    for airport in airports:
        dist = distance(
                (float(airport["lat"]), float(airport["lon"])), 
                (float(lat), float(lon))
        )
        distances.append(dist)
    indeces = numpy.argsort(distances)
    closest_airports = numpy.take(airports, indeces)[:int(num)]
    if not detailed:
        closest_airports = [airport["code"] for airport in closest_airports]
    print(closest_airports)
    return closest_airports

if __name__ == "__main__":
    closest_airport(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])