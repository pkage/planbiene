import React from 'react'
import { useDispatch } from 'react-redux'

import * as tripActions from '../../actions/trips'

const ArtistSearchBox = props => {
    const dispatch = useDispatch()

    const oku = t => {
        if (t.keyCode === 13) {
            dispatch(tripActions.requestSpotifyArtists(t.target.value))
        }
    }

    return (
        <input onKeyUp={oku} placeholder="search..."/>
    )
}

export default ArtistSearchBox

