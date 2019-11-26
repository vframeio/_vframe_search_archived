import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

const initialState = {
  id: getDefaultInt('currentCollection', 1),
  loading: true,
}

export default function collectionMediaReducer(state = initialState, action) {
  switch (action.type) {
    case types.collectionMedia.show:
      if (!action.data || !action.data.res) {
        return {
          loading: false,
          id: 0,
          lookup: new Set(),        
        }
      }
      return {
        loading: false,
        id: action.data.res.id,
        lookup: new Set(action.data.res.media.map(media => media.id))
      }

    case types.collectionMedia.add_media:
      state.lookup.add(action.media_id)
      return {
        ...state,
        lookup: state.lookup,
      }

    case types.collectionMedia.remove_media:
      state.lookup.delete(action.media_id)
      return {
        ...state,
        lookup: state.lookup,
      }

    default:
      return state
  }
}
