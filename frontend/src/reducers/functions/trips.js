import { fromJS } from 'immutable'

import * as tripTypes from '../../constants/trips'
import { defaultTrip } from '../models/trips'

export class TripReducer {
    /**
     * Navigate a page
     */
    static resolveSpotifyConfig(state, action) {
        return state.setIn(['spotify', 'config'], fromJS(action.config))
    }

    /**
     * set the auth token
     */
    static authenticateSpotify(state, action) {
        return state.setIn(['spotify', 'token'], action.token)
    }

    /**
     * resolve a search
     */
    static resolveSearch(state, action) {
        return state.set('searched_artists', fromJS(action.artists))
    }

    /**
     * Add an artist to the list of artists to build a trip from
     */
    static selectArtist(state, action) {
        let obj = state.get('searched_artists').find( o => o.get('id') === action.id)

        if (obj === undefined) {
            console.warn('artist select search returned no results')
            return state
        }

        if (state.get('artists').find( o => o.get('id') === action.id ) !== undefined) {
            console.warn('avoided adding duplicate artist select')
            return state
        }

        return state.set('artists', state.get('artists').push(obj))
    }

    /**
     * Unselect artist
     */
    static unselectArtist(state, action) {
        const index = state.get('artists').findIndex( o => o.get('id') === action.id )
        if (index === -1) {
            console.warn('avoiding deleting an artist not in the artists')
            return state
        }

        // filter out the index
        return state.set('artists', state.get('artists').filter( (v, i) => i !== index) )
    }
}

// hook up to actions

export default function trip(state = defaultTrip, action, opt_reducer = TripReducer) {
    switch (action.type) {
        case tripTypes.TRIP_SPOTIFY_CONFIG_RESOLVED:
            return opt_reducer.resolveSpotifyConfig(state, action)
        case tripTypes.TRIP_SPOTIFY_AUTHENTICATED:
            return opt_reducer.authenticateSpotify(state, action)
        case tripTypes.TRIP_SPOTIFY_ARTISTS_RESOLVED:
            return opt_reducer.resolveSearch(state, action)
        case tripTypes.TRIP_SPOTIFY_ARTISTS_SELECT:
            return opt_reducer.selectArtist(state, action)
        case tripTypes.TRIP_SPOTIFY_ARTISTS_UNSELECT:
            return opt_reducer.unselectArtist(state, action)
        default:
            return state
    }
}

