import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

const initialState = () => ({
  info: { loading: true, features: [], },
  query: { reset: true, },
  results: { reset: true, results: [] },
  infer: { reset: true, },
  options: {
    // query params
    sort: getDefault('search.sort', 'score-asc'),
    limit: getDefaultInt('search.limit', 30),
    jitter: getDefault('search.jitter', false),

    // ui options
    thumbnailSize: getDefault('search.thumbnailSize', 'th'),
    showGraphic: getDefault('search.showGraphic', false),
    groupByHash: getDefault('search.groupByHash', true),
    autoprocess: getDefault('search.autoprocess', true),
    visualization: getDefault('search.visualization', false),
    verbose: getDefault('search.verbose', false),
  }
})

const loadingState = {
  query: {
    loading: true,
  },
  results: {
    reset: true,
  },
  infer: {
  },
  loading: {
    loading: true,
  },
}

export default function searchReducer(state = initialState(), action) {
  // console.log(action.type, action)
  switch (action.type) {
    case types.search.loading:
      if (action.tag === 'query' && action.offset) {
        return {
          ...state,
          query: {
            ...state.query,
            loadingMore: true,
          }
        }
      }
      return {
        ...state,
        [action.tag]: loadingState[action.tag] || loadingState.loading,
      }

    case types.search.loaded:
      return searchLoaderReducer(state, action)

    case types.search.error:
      return {
        ...state,
        [action.tag]: { error: action.err },
      }

    case types.search.panic:
      return {
        ...initialState(),
      }
    
    case types.search.update_option:
      session.set('search.' + action.key, action.value)
      return {
        ...state,
        options: {
          ...state.options,
          [action.key]: action.value,
        }
      }

    case types.search.update_options:
      Object.keys(action.opt).reduce((a,b) => { a['search.' + b] = action.opt[b]; return a }, {})
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

function searchLoaderReducer(state, action) {
  // console.log(action.tag, action.data)
  switch (action.tag) {
    case 'query':
      if (action.offset) {
        return {
          ...state,
          query: {
            query: action.data.query,
          },
          results: {
            results: [
              ...state.results,
              ...action.data.res,
            ],
          },
          loadingMore: false,
        }
      }
      return {
        ...state,
        query: action.data.query,
        results: {
          results: action.data.res
        },
        infer: action.data.infer,
      }

    case 'upload':
      return {
        ...state,
        query: action.data.query,
        results: {
          results: action.data.res,
        },
        infer: action.data.infer,
      }

    case 'info':
      return {
        ...state,
        info: action.data,
        options: {
          ...state.options,
        }
      }

    default:
      state
  }
}
