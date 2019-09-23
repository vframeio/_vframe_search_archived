import { with_type, crud_type } from './api/crud.types'

export const search = with_type('search', [
  'loading', 'loaded', 'error', 'panic', 'update_option', 'update_options',
])

export const collection = crud_type('collection', [])

export const collectionMedia = crud_type('collectionMedia', [
  'load', 'add_media', 'remove_media',
])

export const upload = crud_type('upload', [])

export const feature = crud_type('feature', [])

export const media = crud_type('media', [])

export const modelzoo = crud_type('modelzoo', [ 'asset_load', 'image_load', ])

export const dashboard = with_type('dashboard', [
  'loading', 'loaded', 'error', 'update_option', 'update_options',
])

export const api = with_type('api', [ 'loading', 'loaded', 'error' ])

export const socket = with_type('socket', [
  'connect', 'connect_error',
  'reconnect', 'reconnecting', 'reconnect_error', 'reconnect_failed',
  'disconnect', 'error', 'status',
  'ping_pong_send', 'ping_pong_receive',
  'list_tasks',
  'task_start', 'task_end', 'task_update',
])

export const task = with_type('task', [
  'loading', 'loaded', 'error',
  'starting_task', 'stopping_task',
  'task_begin', 'task_finish',
  'start_queue', 'stop_queue',
  'starting_queue', 'stopping_queue',
  'progress',
])

export const system = with_type('system', [
  'load_site',
  'running_command',
  'command_output',
  'relay_connected',
  'relay_disconnected',
  'rpc_connected',
  'rpc_disconnected',
  'list_directory',
  'listing_directory',
  'count_directory',
  'counting_directory',
  'stdout',
  'stderr',
  'change_language',
])

export const init = '@@INIT'
