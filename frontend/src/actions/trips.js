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

export const requestSpotifyArtists = search => ({
    type: tripTypes.TRIP_SPOTIFY_ARTISTS_REQUESTED,
    search
})

export const resolveSpotifyArtists = artists => ({
    type: tripTypes.TRIP_SPOTIFY_ARTISTS_RESOLVED,
    artists
})

export const selectSpotifyArtist = id => ({
    type: tripTypes.TRIP_SPOTIFY_ARTISTS_SELECT,
    id
})

export const unselectSpotifyArtist = id => ({
    type: tripTypes.TRIP_SPOTIFY_ARTISTS_UNSELECT,
    id
})

export const finalizeArtistList = () => ({
    type: tripTypes.TRIP_SPOTIFY_ARTISTS_DONE
})

export const loadTrip = trip => ({
    type: tripTypes.TRIP_LOADED,
    trip
})
