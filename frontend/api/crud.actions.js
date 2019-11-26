import { crud_fetch } from './crud.fetch'
import { as_type } from './crud.types'
import { upload_action } from './crud.upload'
import { store } from '../store'

export function crud_actions(type) {
  const fetch_type = crud_fetch(type)
  return [
    'index',
    'show',
    'create',
    'update',
    'destroy',
  ].reduce((lookup, param) => {
    lookup[param] = crud_action(type, param, (q) => fetch_type[param](q))
    return lookup
  }, {
    action: (method, fn) => crud_action(type, method, fn),
    upload: (fd) => upload_action(type, fd),
    updateOption: (key, value) => dispatch => {
      dispatch({ type: as_type(type, 'update_option'), key, value })
    },
    updateOptions: opt => dispatch => {
      dispatch({ type: as_type(type, 'update_options'), opt })
    },
  })
}

export const crud_action = (type, method, fn) => q => dispatch => {
  return new Promise ((resolve, reject) => {
    if (method === 'index') {
      if (store.getState()[type].index.loading) {
        return resolve({})
      }
    }
    dispatch({ type: as_type(type, method + '_loading') })
    fn(q).then(data => {
      dispatch({ type: as_type(type, method), data })
      resolve(data)
    }).catch(e => {
      console.log(e)
      dispatch({ type: as_type(type, method + '_error') })
      reject(e)
    })
  })
}
