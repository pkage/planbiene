import React from 'react'
import { useDispatch } from 'react-redux'
import './ArtistSearchBox.css'

import * as tripActions from '../../actions/trips'

const ArtistSearchBox = props => {
    const dispatch = useDispatch()

    const oku = t => {
        if (t.keyCode === 13 && t.target.value.trim() !== '') {
            dispatch(tripActions.requestSpotifyArtists(t.target.value))
        }
    }

    return (
        <input
            className="ArtistSearchBox__input"
            onKeyUp={oku}
            placeholder="search..."
            autoFocus/>
    )
}

export default ArtistSearchBox

