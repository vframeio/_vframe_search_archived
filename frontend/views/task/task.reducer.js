import * as types from '../../types'
import { session, getDefault, getDefaultInt } from '../../session'

import { crudState, crudReducer } from '../../api/crud.reducer'

const initialState = crudState('task', {
  options: {
    // sort: getDefault('task.sort', 'id asc'),
  },
  pingpong: {},
  info: {},
  tasks: {},
})

export default function taskReducer(state = initialState, action) {
  const { uuid } = action.data || {}
  switch (action.type) {
    case types.task.loaded:
      return taskLoaderReducer(state, action)

    case types.socket.ping_pong_send:
      return {
        ...state,
        pingpong: {
          ping: action.time,
        }
      }

    case types.socket.ping_pong_receive:
      return {
        ...state,
        pingpong: {
          ping: state.pingpong.ping,
          pong: action.time,
        }
      }

    case types.socket.task_start:
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [uuid]: { 'debug': "Started " + new Date() },
        }
      }

    case types.socket.task_end:
      const { [uuid]: finished_task, ...ongoingTasks } = state.tasks
      return {
        ...state,
        tasks: ongoingTasks,
      }

    case types.socket.list_tasks:
      return {
        ...state,
        tasks: action.data.tasks,
      }

    case types.socket.task_update:
      console.log(action.data)
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [uuid]: {
            ...state.tasks[uuid],
            [action.data.type]: action.data.data,
          }
        }
      }

    default:
      return state
  }
}

function taskLoaderReducer(state, action) {
  switch (action.tag) {
    case 'info':
      return {
        ...state,
        info: action.data,
      }

    default:
      return state
  }
}
