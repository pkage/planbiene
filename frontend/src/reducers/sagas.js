import { put, takeEvery, takeLatest, all, call } from 'redux-saga/effects'
import * as tripActions from '../actions/trips'
import * as tripTypes  from '../constants/trips'

import * as uiTypes from '../constants/ui'
import * as uiActions from '../actions/ui'
import * as utils from '../utils'

import { store } from '../index'

const BACKEND = 'http://localhost:8000'
const route = path => `${BACKEND}${path}`


function* resolveSpotifyConfig() {
    const cfg = yield fetch(route('/spotify/config')).then(r => r.json())


	yield put(tripActions.resolveSpotifyConfig(cfg))
}

function* watchSpotifyConfigRequest() {
    yield takeLatest(tripTypes.TRIP_SPOTIFY_CONFIG_REQUESTED, resolveSpotifyConfig)
}

// page watching
function* syncPages(action) {

    console.log('syncing pages', action, utils.transformRoute(action.target))


    yield call( () => {} )

}

function* watchPageSync() {
    yield takeEvery(uiTypes.UI_NAVIGATE, syncPages)
}

// spotify smooth auth
function* spotifyAuthenticationPageSync() {
    window.history.pushState({}, '', '/')
    yield put(uiActions.navigate(uiTypes.UI_PAGE_LIST_ARTISTS))
}

function* watchSpotifyAuthentication() {
    yield takeLatest(tripTypes.TRIP_SPOTIFY_AUTHENTICATED, spotifyAuthenticationPageSync)
}

// perform spotify search
function* performSpotifySearch(action) {
    const results = yield utils.spotify('search', {q: action.search, type: 'artist'})

    console.log('results', results)

    yield put(tripActions.resolveSpotifyArtists(results.artists.items))
    
}

function* watchSpotifySearches() {
    yield takeLatest(tripTypes.TRIP_SPOTIFY_ARTISTS_REQUESTED, performSpotifySearch)
}

// final submission
function* requestTrip() {

    yield put( uiActions.navigate( uiTypes.UI_PAGE_LOADING ) )

    const apikey = store.getState().trip.getIn(['spotify', 'token'])
    const artists = store.getState().trip.get('artists').toJS()

    const trip = yield fetch(route('/trip'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: apikey,
            artists
        })
    }).then(r => r.json())

    console.log('resolved trip ', trip)
     
    yield put( tripActions.loadTrip(trip) )

    yield put( uiActions.navigate( uiTypes.UI_PAGE_TRIP ) )
}

function* watchSpotifyDone() {
    yield takeLatest(tripTypes.TRIP_SPOTIFY_ARTISTS_DONE, requestTrip)
}

export default function* rootSaga() {
    yield all([
        watchSpotifyConfigRequest(),
        watchPageSync(),
        watchSpotifyAuthentication(),
        watchSpotifySearches(),
        watchSpotifyDone()
    ])
}
