import * as types from '../../types'
import { store, history } from '../../store'
import { api, post, pad, preloadImage } from '../../util'
import querystring from 'query-string'

// urls

const url = {
  // add_media: (id) => '/api/v1/modelzoo/' + id + '/add/',
  // remove_media: (id, media_id) => '/api/v1/modelzoo/' + id + '/media/' + media_id + '/',
}

export const fetchModelZooFiles = (key, files) => dispatch => {
  files.forEach(fn => {
    console.log(key, fn)
    switch (fn.split('.').pop()) {
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'svg':
        dispatch({
          type: types.modelzoo.image_load,
          fn: "/static/modelzoo/" + key + "/" + fn
        })
        break
      case 'md':
        fetch("/static/modelzoo/" + key + "/" + fn)
        .then(res => res.text())
        .then(data => dispatch({
          type: types.modelzoo.asset_load,
          data,
          fn
        }))
        break
      default:
        break
    }
  })
  // util.allProgress(, (percent, i, n) => {
  //   console.log('pix2pixhd load progress', i, n)
  //   dispatch({
  //     type: types.app.load_progress,
  //     progress: { i, n },
  //     data: { module: 'pix2pixhd' },
  //   })
  // }).then(res => {
  //   const [datasetApiReport, sequences, datasets, checkpoints] = res //, datasets, results, output, datasetUsage, lossReport] = res
}

