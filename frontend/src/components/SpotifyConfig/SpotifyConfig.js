import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { requestSpotifyConfig, authenticateSpotify } from '../../actions/trips'

import { useHistory } from 'react-router-dom'
import { urify } from '../../utils'

const SpotifyConfig = props => {
    const dispatch = useDispatch()
    const history  = useHistory()

    const showLogin = useSelector( store => !store.trip.getIn(['spotify', 'loggedin']) && store.trip.getIn(['spotify', 'config']) !== null)
    const spotifyConfig = useSelector( store => store.trip.getIn(['spotify', 'config']) )
    const spotifyToken = useSelector( store => store.trip.getIn(['spotify', 'token']) )

    // get the config on loading
    useEffect( () => {
        dispatch(requestSpotifyConfig())
    }, [dispatch])

    // if we've got the token do nothing
    if (spotifyToken !== null) {
        return ( <div/> )
    }

    // if we should show a login button
    if (showLogin) {
        const spotifyScope = 'user-read-email'
        const redirect = 'http://localhost:3000/login/redirect/spotify'
        const spotifyLoginURL = `https://accounts.spotify.com/authorize?client_id=${spotifyConfig.get('client_id')}&redirect_uri=${urify(redirect)}&scope=${urify(spotifyScope)}&response_type=token`
        return (
            <a href={spotifyLoginURL}>login with spotify</a>
        )
    }

    // we're returning from the login flow
    if (window.location.href.indexOf('login/redirect/spotify') !== -1 && spotifyToken === null) {
        // hack
        const url = new URL(window.location.href.replace('#', '?'))

        dispatch( authenticateSpotify( url.searchParams.get('access_token') ) )

        history.push('/')
    }

    // loading the initial config
    return (
        <p> loading spotify </p>
    )
}

export default SpotifyConfig
