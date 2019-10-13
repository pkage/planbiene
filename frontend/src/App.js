import React from 'react';

import {
    useSelector
} from 'react-redux'

import {
    UI_PAGE_LIST_ARTISTS,
    UI_PAGE_LOADING
} from './constants/ui'


import {
    transformRoute
} from './utils'

import ArtistsSelect from './components/ArtistsSelect/ArtistsSelect'
import SpotifyConfig from './components/SpotifyConfig/SpotifyConfig'
import Splash from './components/Splash/Splash'
import LoadingScreen from './components/LoadingScreen/LoadingScreen'

function App() {
    // react-router
    const currentPage = useSelector( store => store.ui.get('page') )
    const spotifyKey = useSelector( store => store.trip.getIn(['spotify', 'token']) )

    console.log('current: ', currentPage, transformRoute(currentPage))



    if (spotifyKey === null) {
        return (
            <Splash>
                <SpotifyConfig/>
            </Splash>
        )
    }
    
    if (currentPage === UI_PAGE_LIST_ARTISTS) {
        return <ArtistsSelect/>
    }

    if (currentPage === UI_PAGE_LOADING) {
        return <LoadingScreen/>
    }

    return <p> 404 </p>
    
}

export default App;
