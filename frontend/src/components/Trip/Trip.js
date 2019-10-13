import React from 'react'
import { useSelector } from 'react-redux'
import './Trip.css'

import Globe from '../Globe/Globe'


const Price = props => '€' + (props.price / 100).toFixed(2)
const Flight = props => {
    return (
        <div className="TripFlight">
            <b>{props.info.numbers[0]}</b>
            <p>{props.info.airports.name} &bull; {(new Date(props.info.departure_time*1000).toUTCString())} &bull; <Price price={props.info.price}/></p>
            <a href={props.info.uri} rel="noopener noreferrer" target="_blank" className="Trip__link">book now</a>
        </div>
    )
}

const TripStop = props => {
    console.log(props.info)

    let datetime = new Date(props.info.event.start * 1000)
    datetime = datetime.toTimeString()

    return (
        <div className="TripStop">
            <h2>{props.info.event.name}</h2>
            <p>{props.info.venue.name}, {props.info.venue.city} &bull; <Price price={props.info.event.price_pp}/> &bull; {datetime}</p>
            <a href={props.info.event.url} rel="noopener noreferrer" target="_blank" className="Trip__link">book now</a>
            <hr/>
            <Flight info={props.info.flights.outbound}/>
            <hr/>
            <Flight info={props.info.flights.return}/>
        </div>
    )
}

const TripArtist = props => {


    let events = props.events
        .map((ev, i) => (
            <TripStop
                key={i}
                info={ev}/>
        ))

    return (
        <div>
            <h1>{events.length > 0 ? props.artist : "No Results"}</h1>
            {events}
        </div>
    )
}

const Trip = props => {

    const trip = useSelector( store => store.trip.get('trip').toJS() )
    if (trip === null) {
        return <p> trip is null </p>
    }

    const stops = Object.keys(trip.artists)
        .map( key => (
            <TripArtist
                artist={key}
                key={key}
                events={trip.artists[key]}/>
        ))


    return (
        <div className="Trip">
            <div className="Trip__left">
                {stops}
            </div>
            <div className="Trip__right">
                <Globe results={trip.artists} user_data={trip.user_details}/>
            </div>
        </div>
    )
}

export default Trip
