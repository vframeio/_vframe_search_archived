import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import querystring from 'query-string'
import { socket } from '../../socket/socket.connection'

import { crud_fetch } from '../../api/crud.fetch'
import { crud_action } from '../../api/crud.actions'

const url = {
  info: () => process.env.API_HOST + '/api/v1/task/info/',
  long_task: () => process.env.API_HOST + '/api/v1/task/test/',
  download_model: () => process.env.API_HOST + '/api/v1/task/download_model/',
  run: () => process.env.API_HOST + '/api/v1/task/run/',
}

export const info = () => dispatch => (
  api(dispatch, types.task, 'info', url.info())
)

export const run_task = (task_name, params={}) => dispatch => (
  post(dispatch, types.task, task_name, url.run(), { task_name, params })
)

export const ping = () => dispatch => {
  socket.emit("pingpong")
  store.dispatch({ type: types.socket.ping_pong_send, time: Date.now() })
}

// tasks

export const long_task = () => dispatch => (
  run_task('long_task')(dispatch)
)

export const download_model = name => dispatch => (
  run_task('download_model', { name: name })(dispatch)
)

export const update_index = name => dispatch => (
  run_task('update_index')(dispatch)
)

