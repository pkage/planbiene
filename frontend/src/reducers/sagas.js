import { put, takeLatest, all } from 'redux-saga/effects'
import * as tripActions from '../actions/trips'
import * as tripTypes  from '../constants/trips'

const BACKEND = 'http://localhost:8000'
const route = path => `${BACKEND}${path}`


function* resolveSpotifyConfig() {
    const cfg = yield fetch(route('/spotify/config')).then(r => r.json())


	yield put(tripActions.resolveSpotifyConfig(cfg))
}

function* watchSpotifyConfigRequest() {
    yield takeLatest(tripTypes.TRIP_SPOTIFY_CONFIG_REQUESTED, resolveSpotifyConfig)
}

export default function* rootSaga() {
    yield all([
        watchSpotifyConfigRequest()
    ])
}
