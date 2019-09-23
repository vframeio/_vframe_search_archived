import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('feature', {
  currentFeature: {
    loading: false,
    data: {},
  },
  options: {
    sort: getDefault('feature.sort', 'id asc'),
  }
})

const reducer = crudReducer('feature')

export default function featureReducer(state = initialState, action) {
  state = reducer(state, action)
  switch (action.type) {

    case types.feature.loading:
      return {
        ...state,
        currentFeature: {
          loading: true,
        }
      }

    case types.feature.loaded:
      console.log(action.data)
      return {
        ...state,
        currentFeature: action.data
      }

    case types.feature.error:
      return {
        ...state,
        currentFeature: {
          loading: false,          
        }
      }
      
    default:
      return state
  }
}
