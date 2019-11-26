import io from 'socket.io-client'
import { store } from '../store'
import * as types from '../types'

export const socket = io()
socket.emit('join', { room: '/client' })

// export const socket = { on: () => {} }

// SOCKET ACTIONS

socket.on('connect', () => store.dispatch({ type: types.socket.connect }))
socket.on('connect_error', (error) => store.dispatch({ type: types.socket.connect_error, error }))
socket.on('reconnect', (attempt) => store.dispatch({ type: types.socket.reconnect, attempt }))
socket.on('reconnecting', () => store.dispatch({ type: types.socket.reconnecting }))
socket.on('reconnect_error', (error) => store.dispatch({ type: types.socket.reconnect_error, error }))
socket.on('reconnect_failed', (error) => store.dispatch({ type: types.socket.reconnect_failed, error }))
socket.on('disconnect', () => store.dispatch({ type: types.socket.disconnect }))
socket.on('error', (error) => store.dispatch({ type: types.socket.error, error }))
