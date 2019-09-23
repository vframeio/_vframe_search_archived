import * as types from '../types'
import { getOrderedIds, getOrderedIdsFromLookup } from '../util'
import { session } from '../session'

export const crudState = (type, options) => ({
  index: {},
  show: {},
  create: {},
  update: {},
  destroy: {},
  lookup: [],
  ...options,
})

export const crudReducer = (type) => {
  const crud_type = types[type]
  return (state, action) => {
    switch (action.type) {
      // index
      case crud_type.index_loading:
        return {
          ...state,
          index: { loading: true },
        }
      case crud_type.index:
        if (action.data.res.length) {
          return {
            ...state,
            index: {
              lookup: action.data.res.reduce((a, b) => { a[b.id] = b; return a }, {}),
              order: getOrderedIds(action.data.res, state.options.sort),
            },
          }
        } else {
          Object.keys(action.data.res).forEach(key => {
            const el = action.data.res[key]
            el.key = key
            el.id = el.id || key
          })
          return {
            ...state,
            index: {
              lookup: action.data.res,
              order: getOrderedIdsFromLookup(action.data.res, state.options.sort),
            },
          }
        }
      case crud_type.index_error:
        return {
          ...state,
          index: { loading: false, error: true },
        }
      case crud_type.index_sort:
        return {
          ...state,
          index: {
            ...state.index,
            order: action.data.res.map(b => b.id),
          },
        }

      // show
      case crud_type.show_loading:
        return {
          ...state,
          show: { loading: true },
        }
      case crud_type.show:
        if (!action.data) {
          return {
            ...state,
            show: { not_found: true },
          }
        }
        return {
          ...state,
          show: action.data,
        }
      case crud_type.show_error:
        return {
          ...state,
          show: { loading: false, error: true },
        }

      //
      // create
      case crud_type.create_loading:
        return {
          ...state,
          create: { loading: true },
        }
      case crud_type.create:
        return {
          ...state,
          create: action.data,
          index: addToIndex(state.index, action.data.res, state.options.sort),
        }
      case crud_type.create_error:
        return {
          ...state,
          create: action.data,
        }

      //
      // update
      case crud_type.update_loading:
        return {
          ...state,
          update: { loading: true },
        }
      case crud_type.update:
        return {
          ...state,
          update: action.data,
        }
      case crud_type.index_error:
        return {
          ...state,
          update: { loading: false, error: true },
        }

      //
      // destroy
      case crud_type.destroy_loading:
        return {
          ...state,
          destroy: { loading: true },
        }
      case crud_type.destroy:
        return {
          ...state,
          index: {
            ...(() => {
              if (!state.index.lookup) {
                return {}
              }
              delete state.index.lookup[action.data.id]
              const _id = parseInt(action.data.id)
              state.index.order = state.index.order.filter(id => id !== _id)
              return { ...state.index }
            })()
          },
          destroy: { loading: false },
        }
      case crud_type.destroy_error:
        return {
          ...state,
          destroy: { error: true },
        }

      //
      // options
      case crud_type.update_option:
        session.set(type + "." + action.key, action.value)
        return {
          ...state,
          options: {
            ...state.options,
            [action.key]: action.value,
          }
        }

      case crud_type.update_options:
        session.setAll(
          Object.keys(action.opt).reduce((a,b) => { a[type + '.' + b] = action.opt[b]; return a }, {})
        )
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
}

const addToIndex = (index, data, sort) => {
  const lookup = (index && index.lookup) ? {
    ...index.lookup,
  } : {}
  lookup[data.id] = data
  const order = getOrderedIdsFromLookup(lookup, sort)
  return { lookup, order }
}
