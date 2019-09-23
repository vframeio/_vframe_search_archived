import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

const initialState = () => ({
  mediaInfo: {},
  options: {
    // currentFeature: getDefault('currentFeature', null),
  }
})

const loadingState = {
}

export default function dashboardReducer(state = initialState(), action) {
  switch (action.type) {
    case types.dashboard.loading:
      return {
        ...state,
        [action.tag]: loadingState[action.tag] || loadingState.loading,
      }

    case types.dashboard.loaded:
      return {
        ...state,
        [action.tag]: action.data,
      }

    case types.dashboard.error:
      return {
        ...state,
        [action.tag]: { error: action.err },
      }

    case types.dashboard.update_option:
      session.set(action.key, action.value)
      return {
        ...state,
        options: {
          ...state.options,
          [action.key]: action.value,
        }
      }

    case types.dashboard.update_options:
      session.setAll(action.opt)
      return {
        ...state,
        options: {
          ...action.opt,
        }
      }

    default:
      return state
  }
}

