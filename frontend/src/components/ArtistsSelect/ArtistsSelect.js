import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import classNames from 'classnames'
import './ArtistsSelect.css'

import * as tripActions from '../../actions/trips'

import ArtistSearchBox from './ArtistSearchBox'
import Artist from './Artist'

const ArtistsSelect = props => {
    const dispatch = useDispatch()
    // first, get some artists

    const selectedArtists = useSelector( store => store.trip.get('artists') )
    const searchResults = useSelector( store => store.trip.get('searched_artists') )
    const searchQuery = useSelector( store => store.trip.get('search') )

    const selectArtist = id => () => dispatch(tripActions.selectSpotifyArtist(id))
    const unselectArtist = id => () => dispatch(tripActions.unselectSpotifyArtist(id))


    const results = searchResults
        .toJS()
        .map( obj => (
            <Artist
                obj={obj}
                key={obj.id}
                onClick={selectArtist(obj.id)}/>
        ))

    const itinerary = selectedArtists
        .toJS()
        .map( obj => (
            <Artist
                obj={obj}
                key={obj.id}
                onClick={unselectArtist(obj.id)}/>
        ))



    const finalize = () => (itinerary.length !== 0 && dispatch(tripActions.finalizeArtistList()))

    const doneButtonClasses = classNames(
        'ArtistsSelect__done',
        {'ArtistsSelect__done--active': itinerary.length !== 0}
    )

    return (
        <div className="ArtistsSelect">
            <div className="ArtistsSelect__topbar">
                <ArtistSearchBox/>
                <div
                    className={doneButtonClasses}
                    onClick={finalize}>
                    next
                </div>
            </div>
            <div className="ArtistsSelect__grid">
                <div className="ArtistsSelect__list ArtistsSelect__list--results">
                    {results.length !== 0 ? (
                        <ul>
                            {results}
                        </ul>
                    ) : ( searchQuery === '' ?  
                        <i className="ArtistsSelect__ghost">No searches yet.</i> :
                        <i className="ArtistsSelect__ghost">No searches yet.</i> 
                    )}
                </div>
                <div className="ArtistsSelect__list ArtistsSelect__list--itinerary">
                    {itinerary.length !== 0 ? (
                        <ul>
                            {itinerary}
                        </ul>
                    ) : (
                        <i className="ArtistsSelect__ghost">No itinerary yet.</i>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ArtistsSelect
