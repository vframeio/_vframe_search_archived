// import { dispatch } from '../store'
// import * as types from '../types'
// import { socket } from './socket.connection'

// socket.on('system_res', (data) => {
//   // console.log('system response', data)
//   switch (data.type) {
//     case 'relay_connected':
//       return dispatch({
//         type: types.system.relay_connected
//       })
//     case 'relay_disconnected':
//       return dispatch({
//         type: types.system.relay_disconnected
//       })
//     case 'rpc_connected':
//       return dispatch({
//         type: types.system.rpc_connected,
//         runner: data.runner,
//       })
//     case 'rpc_disconnected':
//       return dispatch({
//         type: types.system.rpc_disconnected
//       })
//     case 'relay_status':
//       return dispatch({
//         type: data.rpc_connected ? types.system.rpc_connected : types.system.rpc_disconnected,
//         runner: data.runner,
//       })
//     case 'site':
//       return dispatch({
//         type: types.system.load_site,
//         site: data.site,
//       })
//     default:
//       break
//   }
// })

