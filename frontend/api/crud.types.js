
export const as_type = (a, b) => [a, b].join('_').toUpperCase()

export const with_type = (type, actions) =>
  actions.reduce((a, b) => (a[b] = as_type(type, b)) && a, {})

export const crud_type = (type, actions=[]) =>
  with_type(type, actions.concat([
    'index_loading',
    'index',
    'index_error',
    'index_sort',
    'show_loading',
    'show',
    'show_error',
    'create_loading',
    'create',
    'create_error',
    'update_loading',
    'update',
    'update_error',
    'destroy_loading',
    'destroy',
    'destroy_error',
    'upload_loading',
    'upload_progress',
    'upload_waiting',
    'upload_complete',
    'upload_error',
    'sort',
    'update_option',
    'update_options',
    'loading',
    'loaded',
    'error',
  ]))
