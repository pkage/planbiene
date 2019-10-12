import { combineReducers } from 'redux';
import ui from './functions/ui'
import trip from './functions/trips'

const rootReducer = combineReducers({
    ui,
    trip
})

export default rootReducer

