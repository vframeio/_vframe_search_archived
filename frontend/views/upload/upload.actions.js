import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import actions from '../../actions'
import { session } from '../../session'

export const upload = file => dispatch => {
  const formData = {
    'image': file,
    'username': session('username'),
  }
  // console.log(formData)
  return actions.upload.upload(formData).then(data => {
    // console.log(data.res)
    return data.res
  })
}
