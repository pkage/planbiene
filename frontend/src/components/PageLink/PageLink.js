import React from 'react'

import { useDispatch } from 'react-redux'
import * as uiActions from '../../actions/ui'
import { Link } from 'react-router-dom'
import { transformRoute } from '../../utils'

const PageLink = props => {
    const dispatch = useDispatch()

    return (
        <Link to={transformRoute(props.to)} onClick={() => dispatch(uiActions.navigate(props.to))}>
            {props.children}
        </Link>
    )
}

export default PageLink
