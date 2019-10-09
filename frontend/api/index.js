import { crud_actions } from './crud.actions'
import util from '../util'

/*
for our crud events, create corresponding actions
the actions fire a 'loading' event, call the underlying api method, and then resolve.
so you can do ...
  import { folderActions } from '../../api'
  folderActions.index({ module: 'samplernn' })
  folderActions.show(12)
  folderActions.create({ module: 'samplernn', name: 'foo' })
  folderActions.update(12, { module: 'pix2pix' })
  folderActions.destroy(12, { confirm: true })
  folderActions.upload(12, form_data)
*/

export { util }

export const actions = [
  'collection',
  'upload',
  'media',
  'feature',
  'modelzoo',
].reduce((a,b) => (a[b] = crud_actions(b)) && a, {})
