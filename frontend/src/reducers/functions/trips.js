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
}

// hook up to actions

export default function trip(state = defaultTrip, action, opt_reducer = TripReducer) {
    switch (action.type) {
        case tripTypes.TRIP_SPOTIFY_CONFIG_RESOLVED:
            return opt_reducer.resolveSpotifyConfig(state, action)
        case tripTypes.TRIP_SPOTIFY_AUTHENTICATED:
            return opt_reducer.authenticateSpotify(state, action)
        default:
            return state
    }
}

