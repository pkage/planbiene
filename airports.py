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

# lat, lon: latitude/longtitude of the place to find an aiport nearby
def closest_airport(lat, lon):
    airports = get_airports()
    distances = []
    for airport in airports:
        dist = distance(
                (float(airport["lat"]), float(airport["lon"])), 
                (float(lat), float(lon))
        )
        distances.append(dist)
    closest_airport = airports[numpy.argmin(distances)]
    print(closest_airport)
    return closest_airport

if __name__ == "__main__":
    closest_airport(sys.argv[1], sys.argv[2])