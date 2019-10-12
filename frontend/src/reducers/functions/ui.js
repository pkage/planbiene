// import Immutable from 'immutable'

import * as uiTypes from '../../constants/ui'
import { defaultUI } from '../models/ui.js'

export class UiReducer {
    /**
     * Navigate a page
     */
    static navigate(state, action) {
        console.log('page navigated ', action)
        return state.set('page', action.target)
    }
}

// hook up to actions

export default function ui(state = defaultUI, action, opt_reducer = UiReducer) {
    switch (action.type) {
        case uiTypes.UI_NAVIGATE:
            return opt_reducer.navigate(state, action)
        default:
            return state
    }
}
