import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('upload', {
  options: {
    sort: getDefault('upload.sort', 'id-desc'),
  }
})

const reducer = crudReducer('upload')

export default function uploadReducer(state = initialState, action) {
  console.log(action.type, action)
  if (action.type === types.search.loaded && action.tag === 'query') {
    console.log(action.data.infer)
  }
  state = reducer(state, action)
  switch (action.type) {
    default:
      return state
  }
}
