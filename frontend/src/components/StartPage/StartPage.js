import React from 'react'

import PageLink from '../PageLink/PageLink'
import * as uiTypes from '../../constants/ui'

const StartPage = props => {
    return (
        <p>
            start page <PageLink to={uiTypes.UI_PAGE_SPLASH}>swap</PageLink>
        </p>
    )
}

export default StartPage
