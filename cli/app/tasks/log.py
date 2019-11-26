from gevent import monkey
monkey.patch_all()

from socketio import Client
from requests import post
import time

# ------------------------------------------------
# Task log

class TaskLog:
  def __init__(self, uuid, url):
    self.uuid = uuid
    self.url = url

  def debug(self, message):
    self.emit('debug', message)

  def error(self, message):
    self.emit('error', message)

  def progress(self, current, total, message):
    self.emit('progress', {
      'current': current,
      'total': total,
      'message': message,
    })

  def done(self):
    pass

# ------------------------------------------------
# Task log that communicates over websocket

class SocketTaskLog(TaskLog):
  def __init__(self, uuid, url):
    self.uuid = uuid
    self.url = url
    # self.io = SocketIO(message_queue='redis://')
    self.io = Client()
    print(">>> Connecting to {}".format(url))
    self.io.connect(url)
    self.io.emit('task_start', {
      'uuid': self.uuid,
    })

  def emit(self, message, data):
    self.io.emit('task_update', {
      'uuid': self.uuid,
      'type': message,
      'data': data,
    })

  def done(self):
    time.sleep(1.5) # pause to make sure buffers are flushed
    self.io.disconnect()

# ------------------------------------------------
# Task log that communicates over HTTP

class HTTPTaskLog(TaskLog):
  def __init__(self, uuid, url):
    self.uuid = uuid
    self.url = url

  def emit(msg, data):
    post(self.url, json=data)
