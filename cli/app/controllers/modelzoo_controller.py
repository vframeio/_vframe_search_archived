from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict
from sqlalchemy.sql.expression import func
from random import randrange
import os

from app.sql.common import db
from app.sql.models.feature_type import FeatureType
from app.settings import app_cfg

class ModelzooView(FlaskView):
  def index(self):
    """
    List all models.
    """
    # medias = Media.query.limit(50)
    # print(medias[0])
    models = {}
    for model_name in app_cfg.MODELZOO_CFG.keys():
      models[model_name] = get_model_cfg(model_name)
    return jsonify({
      'status': 'ok',
      'res': models,
    })

  def name(self, name: str):
    """
    Fetch a single model by name.
    """
    model_cfg = get_model_cfg(name)
    modelzoo_path = os.path.join(app_cfg.DIR_MODELZOO, name)
    print(modelzoo_path)
    if os.path.exists(modelzoo_path):
      model_cfg['modelzoo_files'] = [f for f in os.listdir(modelzoo_path)]
    else:
      model_cfg['modelzoo_files'] = []
    print(model_cfg['modelzoo_files'])
    return jsonify({
      'status': 'ok',
      'res': model_cfg,
    })

def get_model_cfg(model_name):
  model_cfg = app_cfg.MODELZOO_CFG.get(model_name)
  cell = model_cfg.copy()
  is_downloaded = os.path.exists(os.path.join(app_cfg.DIR_MODELS, model_cfg.get('model')))
  cell['downloaded'] = is_downloaded
  return cell
