import * as tripTypes from '../constants/trips.js'

export const requestSpotifyConfig = () => ({
    type: tripTypes.TRIP_SPOTIFY_CONFIG_REQUESTED
})

export const resolveSpotifyConfig = config => ({
    type: tripTypes.TRIP_SPOTIFY_CONFIG_RESOLVED,
    config
})

export const authenticateSpotify = token => ({
    type: tripTypes.TRIP_SPOTIFY_AUTHENTICATED,
    token
})
