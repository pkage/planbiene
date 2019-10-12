import { fromJS } from 'immutable'

export const defaultTrip = fromJS({
    artists: [],
    trip: null,
    search: '',
    searched_artists: [],
    spotify: {
        config: null,
        loggedin: false,
        token: null
    }
})
