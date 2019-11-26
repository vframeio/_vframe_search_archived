import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('collection', {
  options: {
    sort: getDefault('collection.sort', 'id asc'),
  }
})

const reducer = crudReducer('collection')

export default function collectionReducer(state = initialState, action) {
  state = reducer(state, action)
  switch (action.type) {
    default:
      return state
  }
}
