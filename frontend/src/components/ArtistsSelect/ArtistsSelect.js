import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import * as tripActions from '../../actions/trips'

import ArtistSearchBox from './ArtistSearchBox'
import Artist from './Artist'

const ArtistsSelect = props => {
    const dispatch = useDispatch()
    // first, get some artists

    const selectedArtists = useSelector( store => store.trip.get('artists') )
    const searchResults = useSelector( store => store.trip.get('searched_artists') )

    const selectArtist = id => () => dispatch(tripActions.selectSpotifyArtist(id))

    const unselectArtist = id => () => dispatch(tripActions.unselectSpotifyArtist(id))

    const results = searchResults
        .map( obj => obj.toJS() )
        .map( obj => (
            <Artist
                obj={obj}
                key={obj.id}
                onClick={selectArtist(obj.id)}/>
        ))

    const itinerary = selectedArtists
        .map( obj => obj.toJS() )
        .map( obj => (
            <Artist
                obj={obj}
                key={obj.id}
                onClick={unselectArtist(obj.id)}/>
        ))

    const finalize = () => dispatch(tripActions.finalizeArtistList())

    return (
        <div className="ArtistsSelect">
            <ArtistSearchBox/>
            <ul>
                {results}
            </ul>
            <hr/>
            <ul>
                {itinerary}
            </ul>
            <hr/>
            <div onClick={finalize}>done</div>
        </div>
    )
}

export default ArtistsSelect
