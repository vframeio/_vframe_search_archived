import uuidv1 from 'uuid/v1'
import { socket } from './socket.connection'

export const run_system_command = opt => syscall_async('run_system_command', opt)
export const disk_usage         = opt => syscall_async('run_system_command', { cmd: 'du', ...opt })
export const list_directory     = opt => syscall_async('list_directory', opt).then(res => res.files)
export const count_directory    = opt => syscall_async('count_directory', opt).then(res => res.count)
export const list_sequences     = opt => syscall_async('list_sequences', opt).then(res => res.sequences)
export const run_script         = opt => syscall_async('run_script', opt)
export const upload_file        = opt => syscall_async('upload_file', opt)
export const read_file          = opt => syscall_async('read_file', opt).then(res => res.file)
export const thumbnail          = opt => syscall_async('thumbnail', opt).then(res => res.file)

export const syscall_async = (tag, payload, ttl=10000) => {
  ttl = payload.ttl || ttl
  return new Promise( (resolve, reject) => {
    const uuid = uuidv1()
    const timeout = setTimeout(() => {
      socket.off('system_res', cb)
      reject('timeout')
    }, ttl)
    const cb = (data) => {
      if (!data.uuid) return
      if (data.uuid === uuid) {
        clearTimeout(timeout)
        socket.off('system_res', cb)
        resolve(data)
      }
    }
    socket.emit('system', { cmd: tag, payload, uuid })
    socket.on('system_res', cb)
  })
}