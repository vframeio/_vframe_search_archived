import { dispatch } from '../store'
import * as types from '../types'

import { socket } from './socket.connection'

let finishTimeout;

socket.on('task_res', (raw_data) => {
  // does not like the nested task object for some reason..
  let data;
  try {
    if (typeof raw_data === 'string') {
      data = JSON.parse(raw_data)
      if (typeof data === 'string') {
        data = JSON.parse(data)
      }
    } else {
      data = raw_data
    }
  } catch (e) {
    console.warn('problem with json', e)
    return
  }
  if (data.task) {
    dispatch({ type: types.task.update, data: data.task })
  }
  // console.log('task', data.type)
  switch (data.type) {
    case 'start':
      // return dispatch({ type: types.system.rpc_connected, runner: data.runner })
      break
    case 'stop':
      break
    // begin and finish calls often arrive out of order, if the old task was preempted
    case 'task_begin':
      dispatch({ type: types.task.task_begin, task: data.task })
      break
    case 'task_finish':
      dispatch({ type: types.task.task_finish, task: data.task })
      break
    case 'kill':
      break
    case 'stdout':
      return dispatch({ type: types.system.stdout, data })
      break
    case 'stderr':
      return dispatch({ type: types.system.stderr, data })
      break
    case 'add':
      break
    case 'remove':
      break
    case 'start_queue':
      break
    case 'stop_queue':
      break
    case 'list':
      break
    case 'set_priority':
      break
    case 'progress':
      dispatch({ type: types.task.progress, task: data.task })
      break
    case 'epoch':
      dispatch({ type: types.task.epoch, task: data.task })
      break
    case 'task_error':
      return console.log('task error', data)
    default:
      console.log(data)
      return console.log('no such task command', data.type)
  }
})

export function emit(type, task={}, opt={}) {
  socket.emit('task', { type, task, ...opt, })
}

export const add_task = (task, opt={}) => emit('add', task, opt)
export const remove_task = (task, opt={}) => emit('remove', task, opt)
export const start_task = (task, opt={}) => emit('start', task, opt)
export const stop_task = (task, opt={}) => emit('stop', task, opt)
export const start_queue = (opt={}) => emit('start_queue', {}, opt)
export const stop_queue = (opt={}) => emit('stop_queue', {}, opt)
