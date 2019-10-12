import React, { Fragment } from 'react';

import {
    useSelector
} from 'react-redux'

import {
    UI_PAGE_SPLASH,
    UI_PAGE_START,
    UI_PAGE_LIST_ARTISTS
} from './constants/ui'


import {
    transformRoute
} from './utils'

import SplashPage from './components/SplashPage/SplashPage'
import StartPage from './components/StartPage/StartPage'
import ArtistsSelect from './components/ArtistsSelect/ArtistsSelect'


// temp ? 
import SpotifyConfig from './components/SpotifyConfig/SpotifyConfig'


function App() {
    // react-router
    const currentPage = useSelector( store => store.ui.get('page') )
    const spotifyKey = useSelector( store => store.trip.getIn(['spotify', 'token']) )

    console.log('current: ', currentPage, transformRoute(currentPage))

    if (spotifyKey === null) {
        return <SpotifyConfig/>
    }
    
    if (currentPage === UI_PAGE_LIST_ARTISTS) {
        return <ArtistsSelect/>
    }

    return <p> 404 </p>
    
}

export default App;
