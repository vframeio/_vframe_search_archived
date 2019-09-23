from flask import request, jsonify, url_for
from flask_classful import FlaskView, route

from celery.result import AsyncResult
from celery.task.control import inspect

from uuid import uuid4
import os
import time
import tempfile
import numpy as np
import cv2 as cv

from app.settings import app_cfg
from app.sql.common import db
from app.server.decorators import APIError
from app.tasks.celery import celery, tasks, task_classes

class TaskView(FlaskView):
  def index(self):
    return jsonify(tasks)

  @route('/info/', methods=['GET'])
  def info(self):
    """List task queues"""
    i = inspect()
    return jsonify({
      "scheduled": i.scheduled(),
      "active": i.active(),
      "queued": i.reserved(),
    })

  @route('/test/', methods=['GET', 'POST'])
  def test(self):
    if request.json:
      params = request.json['params'] or {}
    else:
      params = {}

    uuid = str(uuid4())
    callback_url = os.getenv('TASK_ENDPOINT') or (url_for('index', _external=True) + 'worker')
    task = task_classes['long_task'].delay(uuid, callback_url, params)
    return jsonify({ 'uuid': uuid }), 202

  @route('/run/', methods=['POST'])
  def run_task(self):
    task_name = request.json['task_name']
    params = request.json['params'] or {}

    if task_name not in task_classes:
      return jsonify({ 'error': 'No such task' }), 500

    # TODO: sanitize params

    if request.json:
      params = request.json['params'] or {}
    else:
      params = {}

    uuid = str(uuid4())
    callback_url = os.getenv('TASK_ENDPOINT') or (url_for('index', _external=True) + 'worker')
    task = task_classes[task_name].delay(uuid, callback_url, params)
    return jsonify({ 'uuid': uuid, 'task_name': task_name }), 202

