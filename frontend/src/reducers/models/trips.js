import { fromJS } from 'immutable'

export const defaultTrip = fromJS({
    artists: [],
    search: '',
    searched_artists: [],
    spotify: {
        config: null,
        loggedin: false,
        token: null
    }
})
