import React from 'react'

import PageLink from '../PageLink/PageLink'
import * as uiTypes from '../../constants/ui'

const SplashPage = props => {
    return (
        <p> splash page <PageLink to={uiTypes.UI_PAGE_START}>swap</PageLink></p>
    )
}

export default SplashPage
