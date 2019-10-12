import { fromJS } from 'immutable'

export const defaultTrip = fromJS({
    artists: [],
    spotify: {
        config: null,
        loggedin: false,
        token: null
    }
})
