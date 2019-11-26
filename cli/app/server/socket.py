from gevent import monkey
monkey.patch_all()

import os
import random
import time
import uuid
from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    current_app
)
from celery import Celery
from flask_socketio import (
    SocketIO,
    Namespace,
    emit,
    join_room,
    leave_room,
    disconnect
)
from app.settings import app_cfg
from app.server.web import create_app
from requests import post
import logging

# import eventlet
# eventlet.monkey_patch()

from gevent import monkey
monkey.patch_all()

from app.tasks.celery import celery

def create_socket():
  app = create_app()
  socketio = SocketIO(app, message_queue=app_cfg.SOCKETIO_MESSAGE_QUEUE, async_mode='gevent', logger=False)

  app.clients = {}
  active_tasks = {}

  # ------------------------------------------------
  # clients

  @socketio.on('status')
  def events_message(message):
      emit('status', {'key': message['status']})

  @socketio.on('disconnect request')
  def disconnect_request():
      emit('status', {'key': 'disconnected'})
      disconnect()

  @socketio.on('connect')
  def events_connect():
      userid = str(uuid.uuid4())
      session['userid'] = userid
      print('connected', userid)
      current_app.clients[userid] = request.namespace
      emit('status', {'key': 'connected_user', 'value': userid})

  @socketio.on('disconnect')
  def events_disconnect():
    if 'userid' in session:
      del current_app.clients[session['userid']]
      print('Client %s disconnected' % session['userid'])
    if 'worker' in session:
      uuid = session['worker']
      del active_tasks[uuid]
      emit('task_end', { 'uuid': uuid }, room='/client')

  @socketio.on('pingpong')
  def worker_on_message():
    emit('pingpong', { 'type': 'PING PONG!!!' })

  @socketio.on('join')
  def on_join(data):
    room = data['room']
    join_room(room)
    if room == '/client':
      emit('list_tasks', { 'tasks': active_tasks })

  @socketio.on('leave')
  def on_leave(data):
    room = data['room']
    leave_room(room)

  # ------------------------------------------------
  # workers

  @socketio.on('task_start')
  def on_task_start(data):
    uuid = data['uuid']
    active_tasks[uuid] = {}
    session['worker'] = uuid
    emit('task_start', { 'uuid': uuid }, room='/client')

  @socketio.on('task_update')
  def on_message(data):
    uuid = data['uuid']
    if uuid in active_tasks:
      type = data['type']
      active_tasks[uuid][type] = data['data']
    emit('task_update', data, room='/client')

  # ------------------------------------------------
  # silence logging

  logging.getLogger('socketio').setLevel(logging.ERROR)
  logging.getLogger('engineio').setLevel(logging.ERROR)

  # Initialize Celery
  # celery = Celery(app.name, broker=app_cfg['CELERY_BROKER_URL'])
  # celery.conf.update(app.config)

  socketio.run(app, host='0.0.0.0', port=5000)

