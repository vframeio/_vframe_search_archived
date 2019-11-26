import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('modelzoo', {
  options: {
    sort: getDefault('modelzoo.sort', 'id asc'),
  }
})

const reducer = crudReducer('modelzoo')

export default function modelzooReducer(state = initialState, action) {
  state = reducer(state, action)
  switch (action.type) {
    // reset assets when we navigate
    case types.modelzoo.show:
      return {
        ...state,
        assets: {},
        images: {},
      }
    
    // receive new markdown :)
    case types.modelzoo.asset_load:
      return {
        ...state,
        assets: {
          ...state.assets,
          [action.fn]: action.data,
        },
      }

    case types.modelzoo.image_load:
      return {
        ...state,
        images: {
          ...state.images,
          [action.fn]: true,
        },
      }

    default:
      return state
  }
}
