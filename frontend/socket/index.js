import { store } from '../store'
import * as types from '../types'

import { socket } from './socket.connection'
import * as actions from './socket.actions'
// import * as system from './socket.system'
// import * as live from './socket.live'
import * as task from './socket.task'
// import * as api from './socket.api'

export default {
  socket,
  actions,
  // system,
  // live,
  task,
  // api,
}

socket.on('status', (data) => {
  if (!data) {
    console.log('got empty status')
    return
  }
  console.log('got status', data)
  store.dispatch({ type: types.socket.status, ...data })
  // switch (data.key) {
  //   case 'processing':
  //     // store.dispatch({
  //     //   type: 'SET_PARAM',
  //     //   ...data,
  //     // })
  //     break
  //   default:
  //     break
  // }
})

socket.on('list_tasks', (data) => {
  store.dispatch({ type: types.socket.list_tasks, data })
})

socket.on('task_start', (data) => {
  store.dispatch({ type: types.socket.task_start, data })
})

socket.on('task_update', (data) => {
  store.dispatch({ type: types.socket.task_update, data })
})

socket.on('task_end', (data) => {
  store.dispatch({ type: types.socket.task_end, data })
})

socket.on('pingpong', data => {
  store.dispatch({ type: types.socket.ping_pong_receive, time: Date.now() })
})