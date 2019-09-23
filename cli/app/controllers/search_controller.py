from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict
from sqlalchemy.sql.expression import func
from random import randrange

import cv2 as cv
import time

from app.sql.common import db, Session
from app.sql.models.feature_type import FeatureType
from app.sql.models.media import Media
from app.sql.models.media_feature import MediaFeature
from app.sql.models.upload import Upload
from app.indexes.single_feature_index import SingleFeatureIndex

feature_index = SingleFeatureIndex()

class SearchView(FlaskView):
  def info(self):
    """
    Identify the active model
    """
    if feature_index.index is None:
      return self.load(1)
      # return jsonify({
      #   'status': 'unloaded',
      #   'res': {
      #     'feature': {},
      #   }
      # })

    if feature_index.loading:
      return jsonify({
        'status': 'loading',
        'res': {
          'feature': feature_index.feature_type.toJSON(),
        }
      })
    res = {
      'model': feature_index.cvmodel.dnn_cfg,
      'feature': feature_index.feature_type.toJSON(),
    }
    if feature_index.detection_model is not None:
      res['detection_model'] = feature_index.detection_model.dnn_cfg
    else:
      res['detection_model'] = {}

    return jsonify({
      'status': 'ok',
      'res': res
    })

  def load(self, id):
    """
    Reload the active search model
    """
    feature_type = FeatureType.query.get(id)
    if feature_type:
      feature_index.load(feature_type)
      return jsonify({
        'status': 'ok',
        'res': {
          'model': feature_index.cvmodel.dnn_cfg,
          'feature': feature_type.toJSON(),
        }
      })
    return jsonify({
      'status': 'unloaded',
      'res': {}
    })


  def load_detection_model(self, key: str):
    """
    Reload the active detection model
    """
    feature_index.load_detection_model(key)
    return jsonify({
      'status': 'ok',
      'res': {
        'model': feature_index.cvmodel.dnn_cfg,
        'feature': feature_type.toJSON(),
      }
    })

  def media(self, id):
    """
    Query the model with existing media (by id)
    """
    start_time = time.time()
    media = Media.query.get(id)
    if media is None:
      return jsonify({
        'status': 'error',
        'error': "Upload not found",
      })
    path = media.fullpath()
    im = cv.imread(path)
    results = feature_index.query(im)
    infer = feature_index.infer(im)

    return jsonify({
      'status': 'ok',
      'query': {
        'media': media.toJSON(),
        'timing': time.time() - start_time,
      },
      'res': results,
      'infer': infer.toJSON() if infer else {},
    })

  def sha256(self, hash: str):
    """
    Query the model with existing media (by hash)
    """
    start_time = time.time()
    media = Media.query.filter(_and(Media.sha256 == hash, Media.parent_id is None)).first()
    if media is None:
      return jsonify({
        'status': 'error',
        'error': "Upload not found",
      })
    path = media.fullpath()
    im = cv.imread(path)
    results = feature_index.query(im)
    infer = feature_index.infer(im)

    return jsonify({
      'status': 'ok',
      'query': {
        'media': media.toJSON(),
        'timing': time.time() - start_time,
      },
      'res': results,
      'infer': infer.toJSON() if infer else {},
    })

  def upload(self, id):
    """
    Query the model with something we already uploaded
    """
    start_time = time.time()
    upload = Upload.query.get(id)
    if upload is None:
      return jsonify({
        'status': 'error',
        'error': "Upload not found",
      })
    path = upload.fullpath()
    im = cv.imread(path)
    results = feature_index.query(im)
    infer = feature_index.infer(im)

    return jsonify({
      'status': 'ok',
      'query': {
        'upload': upload.toJSON(),
        'timing': time.time() - start_time,
      },
      'res': results,
      'infer': infer.toJSON() if infer else {},
    })

  def random(self, seed: str):
    """
    Fetches a random media w/ seed
    """
    start_time = time.time()
    count = db.session.query(Media).count()
    if count == 0:
      return jsonify({ 'status': 'error', 'error': 'Database empty' })

    if seed:
      rand = int(seed, 16) % count
    else:
      rand = randrange(0, count)
    while True:
      media = db.session.query(Media)[rand]         # FIXME: convert to MediaFeature
      if media.mediaType == 'image' or media.mediaType == 'video_frame':
        break
      else:
        rand = randrange(0, count)
    path = media.fullpath()
    im = cv.imread(path)
    results = feature_index.query(im)
    im = cv.imread(path)
    infer = feature_index.infer(im)
    # print(infer)

    return jsonify({
      'status': 'ok',
      'query': {
        'media': media.toJSON(),
        'timing': time.time() - start_time,
      },
      'res': results,
      'infer': infer.toJSON() if infer else {},
    })
