import os
import logging
import logging.handlers

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("flask.log",
    maxBytes=3000000, backupCount=2)
formatter = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler())

logging.debug("starting app")

from flask import Flask, Blueprint, jsonify, send_from_directory, request
from app.sql.common import db, connection_url

from app.settings import app_cfg
from app.controllers.collection_controller import CollectionView
from app.controllers.modelzoo_controller import ModelzooView
from app.controllers.feature_controller import FeatureView
from app.controllers.search_controller import SearchView, feature_index
from app.controllers.socket_controller import SocketView
from app.controllers.upload_controller import UploadView
from app.controllers.media_controller import MediaView
from app.controllers.task_controller import TaskView

def create_app(script_info=None):
  """
  functional pattern for creating the flask app
  """
  app = Flask(__name__, static_folder=app_cfg.DIR_STATIC, static_url_path='/static')
  app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['CELERY_BROKER_URL'] = app_cfg.CELERY_BROKER_URL
  app.config['CELERY_RESULT_BACKEND'] = app_cfg.CELERY_RESULT_BACKEND

  db.init_app(app)

  CollectionView.register(app, route_prefix='/api/v1/')
  ModelzooView.register(app, route_prefix='/api/v1/')
  FeatureView.register(app, route_prefix='/api/v1/')
  SearchView.register(app, route_prefix='/api/v1/')
  SocketView.register(app, route_prefix='/api/v1/')
  UploadView.register(app, route_prefix='/api/v1/')
  MediaView.register(app, route_prefix='/api/v1/')
  TaskView.register(app, route_prefix='/api/v1/')

  feature_index.initialize()

  index_html = 'prod.html' if app_cfg.PRODUCTION else 'dev.html'

  @app.errorhandler(404)
  def page_not_found(e):
    return app.send_static_file(index_html), 200
    # path = os.path.join(os.path.dirname(__file__), './static/index.html')
    # with open(path, "r") as f:
    #   return f.read(), 200

  @app.route('/', methods=['GET'])
  def index():
    return app.send_static_file('index.html')

  @app.route('/favicon.ico')
  def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img/'),
      'favicon.ico',mimetype='image/vnd.microsoft.icon')

  @app.shell_context_processor
  def shell_context():
    return { 'app': app, 'db': db }

  return app
