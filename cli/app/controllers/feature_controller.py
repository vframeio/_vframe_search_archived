from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict
from sqlalchemy.sql.expression import func
from random import randrange
import os

from app.sql.common import db
from app.sql.models.feature_type import FeatureType, FeatureTypeForm
from app.settings import app_cfg

from app.controllers.crud_controller import CrudView

class FeatureView(CrudView):
  model = FeatureType
  form = FeatureTypeForm

  # def on_index(self, data):
  #   # for model_name in app_cfg.MODELZOO_CFG.keys():
  #   #   models[model_name] = get_model_cfg(model_name)
  #   return jsonify({
  #     'status': 'ok',
  #     'res': featureTypes,
  #   })
  #   return data

def get_model_cfg(model_name):
  model_cfg = app_cfg.MODELZOO_CFG.get(model_name)
  cell = model_cfg.copy()
  is_downloaded = os.path.exists(os.path.join(app_cfg.DIR_MODELS, model_cfg.get('model')))
  cell['downloaded'] = is_downloaded
  return cell
