import fetch from 'node-fetch'

export function crud_fetch(type, tag) {
  const uri = '/api/v1/' + type + '/' + (tag || '')
  return {
    index: q => {
      return fetch(_get_url(uri, q), _get_headers())
        .then(req => req.json())
        .catch(error)
    },
    
    show: id => {
      return fetch(uri + id + '/', _get_headers(), _get_headers())
        .then(req => req.json())
        .catch(error)
    },
    
    create: data => {
      return fetch(uri, post(data))
        .then(req => req.json())
        .catch(error)
    },

    update: data => {
      return fetch(uri + data.id + '/', put(data))
        .then(req => req.json())
        .catch(error)
    },

    destroy: data => {
      return fetch(uri + data.id + '/', destroy(data))
        .then(req => req.json())
        .catch(error)
    },
  }
}

function _get_url(_url, data) {
  const url = new URL(window.location.origin + _url)
  if (data) {
    Object.keys(data).forEach(key => url.searchParams.append(key, data[key]))
  }
  return url
}
export function _get_headers() {
  return {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
    },
  }
}
export function post(data) {
  return {
    method: 'POST',
    body: JSON.stringify(data),
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  }
}
export function postBody(data) {
  return {
    method: 'POST',
    body: data,
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
    },
  }
}
export function put(data) {
  return {
    method: 'PUT',
    body: JSON.stringify(data),
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  }
}
export function destroy(data) {
  return {
    method: 'DELETE',
    body: JSON.stringify(data),
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  }
}
function error(err) {
  console.warn(err)
}
