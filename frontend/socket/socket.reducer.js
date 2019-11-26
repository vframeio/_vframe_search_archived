import * as types from '../types'

const socketInitialState = {
  loading: false,
  error: null,

  socket: {
    connected: false,
    status: "disconnected",
    error: null,
  }
}

export default function socketReducer(state = socketInitialState, action) {
  let processor = null
  switch(action.type) {
    case types.socket.connect:
    case types.socket.reconnecting:
      return {
        status: 'connected',
        connected: true,
        error: null,
      }
    case types.socket.reconnect:
      return {
        status: 'reconnecting (attempt ' + action.attempt + ')',
        connected: false,
        error: null,
      }
    case types.socket.connect_error:
    case types.socket.reconnect_error:
    case types.socket.disconnect:
    case types.socket.reconnect_failed:
      return {
        status: 'disconnected',
        connected: false,
        error: action.error || null,
      }
    case types.socket.error:
      return {
        ...state,
        error: action.error,
      }
    default:
      return state
  }
}