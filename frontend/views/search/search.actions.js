import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import querystring from 'query-string'

import * as uploadActions from '../upload/upload.actions'

const url = {
  info: () => process.env.API_HOST + '/api/v1/search/info/',
  searchMedia: (media_id) => process.env.API_HOST + '/api/v1/search/media/' + media_id + '/',
  searchRandom: (seed) => process.env.API_HOST + '/api/v1/search/random/' + (seed ? seed + '/' : ""),
  searchSha256: (hash) => process.env.API_HOST + '/api/v1/search/sha256/' + hash + '/',
  searchUpload: (upload_id) => process.env.API_HOST + '/api/v1/search/upload/' + upload_id + '/',
}

export const upload = image => dispatch => {
  uploadActions.upload(image)(dispatch).then(data => {
    return searchUpload(data.id)(dispatch)
  }).catch((err, data) => {
    // console.log(err, data)
  })
}

export const panic = () => dispatch => {
  history.push('/search/')
  dispatch({ type: types.search.panic })
}
export const updateOption = (key, value) => dispatch => {
  dispatch({ type: types.search.update_option, key, value })
}
export const updateOptions = opt => dispatch => {
  dispatch({ type: types.search.update_options, opt })
}
export const loadCurrentPath = () => dispatch => {
  if (store.getState().search.query.loading) {
    return
  }
  let path = window.location.pathname.split('/')
  if (path.length < 4) return
  const [ _, search, cmd, id, ...rest ] = path
  // console.log(cmd, id)
  switch (cmd) {
    case 'random':
      return searchRandom(id)(dispatch)
    case 'media':
      return searchMedia(id)(dispatch)
    case 'sha256':
      return searchSha256(id)(dispatch)
    case 'upload':
      return searchUpload(id)(dispatch)
  }
}

export const info = () => dispatch => (
  api(dispatch, types.search, 'info', url.info())
)
export const searchMedia = (media_id) => dispatch => (
  api(dispatch, types.search, 'query', url.searchMedia(media_id))
)
export const searchRandom = (seed) => dispatch => (
  api(dispatch, types.search, 'query', url.searchRandom(seed))
)
export const searchSha256 = (hash) => dispatch => (
  api(dispatch, types.search, 'query', url.searchSha256(hash))
)
export const searchUpload = (upload_id) => dispatch => (
  api(dispatch, types.search, 'query', url.searchUpload(upload_id))
)
