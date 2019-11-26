import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import querystring from 'query-string'

// urls

const url = {
  load: (feature_id) => process.env.API_HOST + '/api/v1/search/load/' + feature_id + '/',
}

export const load = (feature_id) => dispatch => (
  api(dispatch, types.feature, 'load', url.load(feature_id))
)
