# GigScanner



## Flight Handler Documentation


### get_bookings function
#### EXAMPLE USAGE:
get_bookings(start="Vilnius", end="Edinburgh" direct=False, when="2020-01", passenger_no=1)
#### MANDATORY FIELDS:
*  start - location to fly from
*  end - location to fly to
#### OPTIONAL FIELDS:
*  direct - direct flights only. defaults to False
*  when - day or month in which the flight should take place. defaults to anytime
* passenger_no - number of passengers for the flight. defaults to 1
#### RETURN OBJECT:
[
    {
        "departure_time" : {departure-timestamp}
        "arrival" : {arrival-timestamp}
        "price" : {cost-in-pence-int}
        "duration" : {duration-in-minutes}
        "uri" : {uri-to-purchase}
        "airports" : [{airport-code}, {airport-code}, ...]
        "numbers" : [{flight-number}, {flight-number}, ...]
    },
    { 
        ...
    },
    ...
]

### get_bookings_both_ways function
#### EVERYTHING SAME AS get_bookings except return object
#### RETURN OBJECT:
{
        "price_pp": {outbound_price} + {return_price},
        "outbound" : {
            "departure_time" : {departure-timestamp}
            "arrival" : {arrival-timestamp}
            "price" : {cost-in-pence-int}
            "duration" : {duration-in-minutes}
            "uri" : {uri-to-purchase}
            "airports" : [{airport-code}, {airport-code}, ...]
            "numbers" : [{flight-number}, {flight-number}, ...]
        },
        "return" : {
            "departure_time" : {departure-timestamp}
            "arrival" : {arrival-timestamp}
            "price" : {cost-in-pence-int}
            "duration" : {duration-in-minutes}
            "uri" : {uri-to-purchase}
            "airports" : [{airport-code}, {airport-code}, ...]
            "numbers" : [{flight-number}, {flight-number}, ...]
        }
}