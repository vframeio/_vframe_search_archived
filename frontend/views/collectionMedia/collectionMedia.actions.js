import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import { session } from '../../session'
import querystring from 'query-string'

import { crud_fetch } from '../../api/crud.fetch'
import { crud_action } from '../../api/crud.actions'

// urls

const url = {
  add_media: (id) => '/api/v1/collection/' + id + '/add/',
  remove_media: (id, media_id) => '/api/v1/collection/' + id + '/media/' + media_id + '/',
}

const collectionMediaFetch = crud_fetch('collection')

export const loadLastCollection = () => dispatch => {
  const collection_id = session('currentCollection')
  load(collection_id)(dispatch)
}

export const load = (collection_id) => dispatch => {
  if (collection_id) {
    session.set('currentCollection', collection_id)
    crud_action('collectionMedia', 'show', collectionMediaFetch.show)(collection_id)(dispatch)
  }
}

export const add_media = (collection_id, media_id) => dispatch => {
  dispatch({ type: types.collectionMedia.add_media, media_id })
  crud_action('collectionMedia', 'create',
    crud_fetch('collection', collection_id + '/media/').create
  )({ collection_id, media_id, username: session('username') })(dispatch)
}

export const remove_media = (collection_id, media_id) => dispatch => {
  dispatch({ type: types.collectionMedia.remove_media, media_id })
  crud_action('collectionMedia', 'destroy',
    crud_fetch('collection', collection_id + '/media/').destroy
  )({ id: media_id })(dispatch)
}
