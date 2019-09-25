from flask import request, jsonify, current_app
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict

from app.sql.common import db

class SocketView(FlaskView):
  def clients(self):
    """
    List currently connected websocket clients. This includes both web clients and workers.
    """
    return jsonify({
      'clients': list(current_app.clients.keys())
    })

  # @route('/event/', methods=['POST'])
  # def event(self):
  #   """Receive messages from a Celery client via HTTP POST"""
  #   userid = request.json['userid']
  #   data = request.json
  #   ns = current_app.clients.get(userid)
  #   # print(data)
  #   if ns and data:
  #     ns.emit('task', data)
  #     return 'ok'
  #   return 'error', 404
