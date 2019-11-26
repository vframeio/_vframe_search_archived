import { api as api_type } from '../types'

import { format, distanceInWords } from 'date-fns'

export const formatDateTime = dateStr => format(new Date(dateStr), 'D MMM YYYY H:mm')
export const formatDate = dateStr => format(new Date(dateStr), 'D MMM YYYY')
export const formatTime = dateStr => format(new Date(dateStr), 'H:mm')
export const formatAge = dateStr => distanceInWords(new Date(dateStr), new Date()) + ' ago.'

/* Mobile check */

export const isiPhone = !!((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)))
export const isiPad = !!(navigator.userAgent.match(/iPad/i))
export const isAndroid = !!(navigator.userAgent.match(/Android/i))
export const isMobile = isiPhone || isiPad || isAndroid
export const isDesktop = !isMobile

const htmlClassList = document.body.parentNode.classList
htmlClassList.add(isDesktop ? 'desktop' : 'mobile')

/* Default image dimensions */

export const widths = {
  th: 160,
  sm: 320,
  md: 640,
  lg: 1280,
}

/* Formatting functions */

const acronyms = 'id url cc sa fp md5 sha256'.split(' ').map(s => '_' + s)
const acronymsUpperCase = acronyms.map(s => s.toUpperCase())

export const formatName = s => {
  acronyms.forEach((acronym, i) => s = s.replace(acronym, acronymsUpperCase[i]))
  return s.replace(/_/g, ' ')
}

// Use to pad frame numbers with zeroes
export const pad = (n, m) => {
  let s = String(n || 0)
  while (s.length < m) {
    s = '0' + s
  }
  return s
}

export const courtesyS = (n, s) => n + ' ' + (n === 1 ? s : s + 's')

export const padSeconds = n => n < 10 ? '0' + n : n

export const timestamp = (n = 0, fps = 25) => {
  n /= fps
  let s = padSeconds(Math.round(n) % 60)
  n = Math.floor(n / 60)
  if (n > 60) {
    return Math.floor(n / 60) + ':' + padSeconds(n % 60) + ':' + s
  }
  return (n % 60) + ':' + s
}

export const percent = n => (n * 100).toFixed(1) + '%'

export const px = (n, w) => Math.round(n * w) + 'px'

export const clamp = (n, a=0, b=1) => n < a ? a : n < b ? n : b

/* URLs */

export const sha256_tree = (sha256, branch_size=2, tree_depth=2) => {
  const tree_size = tree_depth * branch_size
  let tree = ""
  for (var i = 0; i < tree_size; i += branch_size) {
    tree += '/' + sha256.substr(i, branch_size)
  }
  return tree
}

export const imageUrl = (sha256, frame, size = 'th') => [
  'https://' + process.env.S3_HOST + '/v1/media/keyframes',
  sha256_tree(sha256),
  pad(frame, 6),
  size,
  'index.jpg'
].filter(s => !!s).join('/')

export const uploadUri = ({ sha256, ext }) => '/static/data/uploads' + sha256_tree(sha256) + '/' + sha256 + ext
export const metadataUri = (sha256, tag) => '/metadata/' + sha256 + '/' + tag + '/'
export const keyframeUri = (sha256, frame) => '/metadata/' + sha256 + '/keyframe/' + pad(frame, 6) + '/'

export const preloadImage = opt => {
  let { verified, hash, frame, url } = opt
  if (hash && frame) {
    url = imageUrl(verified, hash, frame, 'md')
  }
  const image = new Image()
  let loaded = false
  image.onload = () => {
    if (loaded) return
    loaded = true
    image.onload = null
  }
  // console.log(img.src)
  image.crossOrigin = 'anonymous'
  image.src = url
  if (image.complete) {
    image.onload()
  }
}

/* AJAX */

let cachedAuth = null
let token = ''
let username = ''

export const post = (dispatch, type=api_type, tag, url, data) => {
  let headers
  if (data instanceof FormData) {
    headers = {
      Accept: 'application/json',
    }
  } else if (data) {
    headers = {
      Accept: 'application/json',
      'Content-Type': 'application/json; charset=utf-8',
    }
    data = JSON.stringify(data)
  }

  dispatch({
    type: type.loading,
    tag,
  })
  return fetch(url, {
    method: 'POST',
    body: data,
    headers,
  })
  .then(res => res.json())
  .then(res => dispatch({
    type: type.loaded,
    tag,
    data: res,
  }))
  .catch(err => dispatch({
    type: type.error,
    tag,
    err,
  }))
}

export const api = (dispatch, type=api_type, tag, url, data) => {
  dispatch({
    type: type.loading,
    tag,
  })
  return fetch(url, {
    method: 'GET',
    // mode: 'cors',
  })
  .then(res => res.json())
  .then(res => dispatch({
    type: type.loaded,
    tag,
    data: res,
  }))
  .catch(err => dispatch({
    type: type.error,
    tag,
    err,
  }))
}

/* sorting */

export const numericSort = {
  asc: (a,b) => a[0] - b[0],
  desc: (a,b) => b[0] - a[0],
}
export const stringSort = {
  asc: (a,b) => a[0].localeCompare(b[0]),
  desc: (a,b) => b[0].localeCompare(a[0]),
}
export const orderByFn = (s='name asc') => {
  const [field='name', direction='asc'] = s.split(' ')
  let mapFn, sortFn
  switch (field) {
    case 'id':
      mapFn = a => [parseInt(a.id) || 0, a]
      sortFn = numericSort[direction]
      break
    case 'epoch':
      mapFn = a => [parseInt(a.epoch || a.epochs) || 0, a]
      sortFn = numericSort[direction]
      break
    case 'size':
      mapFn = a => [parseInt(a.size) || 0, a]
      sortFn = numericSort[direction]
      break
    case 'date':
      mapFn = a => [+new Date(a.date || a.created_at), a]
      sortFn = numericSort[direction]
      break
    case 'updated_at':
      mapFn = a => [+new Date(a.updated_at), a]
      sortFn = numericSort[direction]
      break
    case 'priority':
      mapFn = a => [parseInt(a.priority) || parseInt(a.id) || 1000, a]
      sortFn = numericSort[direction]
    case 'name':
    default:
      mapFn = a => [a.name || "", a]
      sortFn = stringSort[direction]
      break
  }
  return { mapFn, sortFn }
}
export const getOrderedIds = (objects, sort) => {
  const { mapFn, sortFn } = orderByFn(sort)
  return objects.map(mapFn).sort(sortFn).map(a => a[1].id)
}
export const getOrderedIdsFromLookup = (lookup, sort) => {
  return getOrderedIds(Object.keys(lookup).map(key => lookup[key]), sort)
}

/* parallel promises */

export const allProgress = (promises, progress_cb) => {
  let d = 0
  progress_cb(0, 0, promises.length)
  promises.forEach((p) => {
    p.then((s) => {
      d += 1
      progress_cb(Math.floor((d * 100) / promises.length), d, promises.length)
      return s
    })
  })
  return Promise.all(promises)
}

