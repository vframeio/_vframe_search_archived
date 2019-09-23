import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import querystring from 'query-string'

// urls

const url = {
  'mediaInfo': '/api/v1/media/info/',
}

export const mediaInfo = () => dispatch => {
  api(dispatch, types.dashboard, 'mediaInfo', url.mediaInfo)
}