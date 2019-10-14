# GigScanner
![logo][Logo\ (DevPost).png]

## Inspiration
We've all been there: your favourite band just started their world tour, and your city is not on the list. You try to find another way to see them, but having 200 tabs open with the prices of flight and concert tickets is getting a bit overwhelming. We have the solution: a web app dedicated to finding the most affordable concert ticket and flight available to you!

## What it does
Access the web interface and login using Spotify. We will then fetch your favourite artists and suggest routes with pricing to go and see them. Alternatively, you can also search to find tickets for a particular artist, and also automatically get an optimal plan designed for yourself.

## How we built it
We fetch the user's favourite artists from the Spotify API. We then query the TicketMaster Discovery API to find the events the artist is to perform at. Using available data, we determine the venue location using Google Places API, pricing for the tickets (converting different currencies using the live exchange rates from Exchange Rates API), closest airports and required travel dates. Input is then passed for Skyscanner's API to determine the cheapest possible combined trips!

## Challenges we ran into
Limitations of the TicketMaster API

Unfortunately, we ran into some issues with drawing EU-wide event data from TicketMaster's API. Events that are sold outside of the .com or .co.uk domains tend to have limited information provided. We ended up having to use multiple helper APIs to generate the required data.

## Accomplishments that we're proud of
Creating Something We'd Actually Use

It's quite rare that something one has created in the space of 36 hours is something they would come back to again... However, we as a team have found that this was genuinely a great solution to a problem we, and the people around us tend to have. Being able to also get suggested concerts through Spotify means it is something we can keep coming back to, even if we don't have any particular events in mind at the time.

## What we learned
Being Independent

Sometimes the tech out there doesn't work, or isn't 100% reliable. Being able to build our own API gives us the ability to control what's going on, and sometimes is the best option available.

## What's next for GigScanner
Extending to support filtering / more flexible travel suggestions; notifications about price changes for your followed gigs or artists; access to International Discovery API integration; support for suggesting accommodation as part of the travel plan, potentially through the use of Booking's API




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
            "airports" : [{
                "code": {airport-code}
                "name": {airport-name}
            }, ...]
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
