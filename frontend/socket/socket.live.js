// import { dispatch } from '../store'
// import * as types from '../types'
// import * as player from '../live/player'

// import { socket } from './socket.connection'

// socket.on('res', (data) => {
//   // console.log('socket:', data.cmd)
//   switch (data.cmd) {
//     case 'get_last_frame':
//       if (data.res !== 'working') {
//         socket.emit('cmd', {
//           cmd: 'get_last_frame',
//         })
//       }
//       break
//     case 'get_params':
//       data.res && dispatch({
//         type: types.socket.load_params,
//         opt: data.res,
//       })
//       data.res && player.toggleFPS(data.res.processing)
//       break
//     case 'list_checkpoints':
//       dispatch({
//         type: types.socket.list_checkpoints,
//         checkpoints: data.res,
//       })
//       break
//     case 'list_all_checkpoints':
//       dispatch({
//         type: types.socket.list_all_checkpoints,
//         checkpoints: data.res,
//       })
//       break
//     case 'list_epochs':
//       dispatch({
//         type: types.socket.list_epochs,
//         epochs: data.res,
//       })
//       break
//     case 'list_sequences':
//       dispatch({
//         type: types.socket.list_sequences,
//         sequences: data.res,
//       })
//       break
//     default:
//       break
//   }
//   // console.log(data)
// })

// socket.on('frame', player.onFrame)

// export function list_checkpoints(module) {
//   socket.emit('cmd', {
//     cmd: 'list_checkpoints',
//     payload: module,
//   })
// }
// export function list_all_checkpoints(module) {
//   socket.emit('cmd', {
//     cmd: 'list_all_checkpoints',
//     payload: module,
//   })
// }
// export function list_epochs(module, checkpoint_name) {
//   socket.emit('cmd', {
//     cmd: 'list_epochs',
//     payload: (module === 'pix2pix' || module === 'pix2wav') ? module + '/' + checkpoint_name : checkpoint_name,
//   })
// }
// export function list_sequences(module) {
//   socket.emit('cmd', {
//     cmd: 'list_sequences',
//     payload: module,
//   })
// }
// export function load_epoch(checkpoint_name, epoch) {
//   console.log(">> SWITCH CHECKPOINT", checkpoint_name, epoch)
//   socket.emit('cmd', {
//     cmd: 'load_epoch',
//     payload: checkpoint_name + ':' + epoch,
//   })
// }
// export function load_sequence(sequence) {
//   socket.emit('cmd', {
//     cmd: 'load_sequence',
//     payload: sequence,
//   })
// }
// export function seek(frame) {
//   socket.emit('cmd', {
//     cmd: 'seek',
//     payload: frame,
//   })
// }
// export function pause(frame) {
//   socket.emit('cmd', {
//     cmd: 'pause',
//   })
// }
// export function play(frame) {
//   socket.emit('cmd', {
//     cmd: 'play',
//   })
// }
// export function get_params() {
//   socket.emit('cmd', {
//     cmd: 'get_params',
//   })
// }
// export function set_param(key, value) {
//   socket.emit('cmd', {
//     cmd: 'set_param',
//     payload: {
//       'key': key,
//       'value': value,
//     }
//   })
// }