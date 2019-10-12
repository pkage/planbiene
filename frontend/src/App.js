import React from 'react';

import {
    useSelector
} from 'react-redux'

import {
    UI_PAGE_SPLASH,
    UI_PAGE_START
} from './constants/ui'

import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

import {
    transformRoute
} from './utils'

import SplashPage from './components/SplashPage/SplashPage'
import StartPage from './components/StartPage/StartPage'

// temp ? 
import SpotifyConfig from './components/SpotifyConfig/SpotifyConfig'


function App() {
    // react-router
    const currentPage = useSelector( store => store.ui.get('page') )

    console.log('current: ', currentPage, transformRoute(currentPage))

    return (
        <Router>
            <Switch>
                <Route exact path={transformRoute(UI_PAGE_SPLASH)}>
                    <SplashPage/>
                </Route>
                <Route exact path={transformRoute(UI_PAGE_START)}>
                    <StartPage/>
                </Route>

            </Switch>
            <SpotifyConfig/>
        </Router>
    );
}

export default App;
