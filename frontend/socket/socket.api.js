// import { dispatch } from '../store'
// import * as types from '../types'
// import { socket } from './socket.connection'

// socket.on('api_res', (data) => {
//   // console.log('system response', data)
//   data = parse(data)
//   const type = types[data.datatype]
//   console.log('api_res', data.type, data.datatype)
//   if (! type) return console.error('socket:api_res bad datatype', data.datatype)
//   switch (data.type) {
//     case 'create':
//       return dispatch({
//         type: type.create,
//         source: 'socket',
//         data: data.data,
//       })
//     case 'update':
//       return dispatch({
//         type: type.update,
//         source: 'socket',
//         data: data.data,
//       })
//     case 'destroy':
//       return dispatch({
//         type: type.destroy,
//         source: 'socket',
//         data: data.data,
//       })
//     default:
//       break
//   }
// })

// function parse (s) {
//   if (typeof s === 'string') {
//     try {
//       const d = JSON.parse(s)
//       return d
//     } catch (e) {
//       console.error('not valid json')
//       return s
//     }
//   }
//   return s
// }