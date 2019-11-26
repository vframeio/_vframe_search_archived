import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('media', {
  options: {
    sort: getDefault('media.sort', 'id asc'),
  }
})

const reducer = crudReducer('media')

export default function mediaReducer(state = initialState, action) {
  state = reducer(state, action)
  switch (action.type) {
    default:
      return state
  }
}
