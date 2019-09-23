import { as_type } from './crud.types'

export function crud_upload(type, data, dispatch) {
  return new Promise( (resolve, reject) => {
    console.log(type, data)
    const { id } = data
    
    const fd = new FormData()

    Object.keys(data).forEach(key => {
      if (key !== 'id') {
        fd.append(key, data[key])
      }
    })

    let url = id ? '/api/' + type + '/v1/' + id + '/'
                 : '/api/v1/' + type + '/'
    console.log(url)

    const xhr = new XMLHttpRequest()
    xhr.upload.addEventListener("progress", uploadProgress, false)
    xhr.addEventListener("load", uploadComplete, false)
    xhr.addEventListener("error", uploadFailed, false)
    xhr.addEventListener("abort", uploadCancelled, false)
    xhr.open("POST", url)
    xhr.send(fd)

    dispatch && dispatch({ type: as_type(type, 'upload_loading')})

    let complete = false

    function uploadProgress (e) {
      if (e.lengthComputable) {
        const percent = Math.round(e.loaded * 100 / e.total) || 0
        if (percent > 99) {
          dispatch && dispatch({
            type: as_type(type, 'upload_waiting'),
            percent,
            [type]: id,
          })
        } else {
          dispatch && dispatch({
            type: as_type(type, 'upload_progress'),
            percent,
            [type]: id,
          })
        }
      }
      else {
        dispatch && dispatch({
          type: as_type(type, 'upload_error'),
          error: 'unable to compute upload progress',
          [type]: id,
        })
      }
    }

    function uploadComplete (e) {
      let parsed;
      try {
        parsed = JSON.parse(e.target.responseText)
      } catch (e) {
        dispatch && dispatch({
          type: as_type(type, 'upload_error'),
          error: 'upload failed',
          [type]: id,
        })
        reject(e)
        return
      }
      dispatch && dispatch({
        type: as_type(type, 'upload_complete'),
        data: parsed,
        [type]: id,
      })
      if (parsed.res) {
        (parsed.res.length ? parsed.res : [parsed.res]).forEach(file => {
          dispatch && dispatch({
            type: as_type('upload', 'create'),
            data: { res: file },
          })
        })
      }
      resolve(parsed)
    }

    function uploadFailed (evt) {
      dispatch && dispatch({
        type: as_type(type, 'upload_error'),
        error: 'upload failed',
        [type]: id,
      })
      reject(evt)
    }

    function uploadCancelled (evt) {
      dispatch && dispatch({
        type: as_type(type, 'upload_error'),
        error: 'upload cancelled',
        [type]: id,
      })
      reject(evt)
    }
  })
}

export const upload_action = (type, data) => dispatch => crud_upload(type, data, dispatch)
