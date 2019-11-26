"""
Extract a feature from the images in the database
"""

import os
import pickle
from glob import glob
import datetime
import pytz
from os.path import join

import cv2 as cv
from sqlalchemy import or_, and_
from sqlalchemy_utc import utcnow
from sqlalchemy import func
from werkzeug.utils import secure_filename

from app.settings import app_cfg
from app.models.types import MediaType, ModelZoo
from app.utils import log_utils, file_utils
from app.sql.common import Session, Media, FeatureType, db

from app.image import cvdnn

def extract_features(log, opt_pagination=50000):
  """Extract features from the images in the database"""

  session = Session()

  feature_types = session.query(FeatureType).filter(FeatureType.active == True)
  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?

  for feature_type in feature_types:

    dnn_cfg = app_cfg.MODELZOO_CFG.get(feature_type.modelzoo_name)

    feats_tag = dnn_cfg.get('features')
    dims_tag = dnn_cfg.get('dimensions')

    if feats_tag and dims_tag:
      log.debug(f'Using model: {feature_type.modelzoo_name} and layer: {feats_tag} {dims_tag}d')
    else:
      log.debug(f'Model {feature_type.modelzoo_name} still needs to be described with features and dimensions')
      continue

    fp_feature_path = join(app_cfg.DIR_FEATURES, feature_type.modelzoo_name)
    fp_manifest_pkls = glob(join(fp_feature_path, '*_manifest.pkl'))

    log.debug("Existing features:")
    log.debug(fp_manifest_pkls)

    process_id = 0

    if len(fp_manifest_pkls) > 0:
      fp_manifest_pkl = fp_manifest_pkls[-1]
      manifest = file_utils.load_pickle(fp_manifest_pkl)
      process_id = manifest['max_id']
      log.debug('Max indexed ID: {}'.format(process_id))

    mediaCount = session.query(func.count(Media.id)).filter(and_(Media.id > process_id, or_(Media.mediaType == 'image', Media.mediaType == 'video_frame'))).scalar()

    if mediaCount == 0:
      log.debug('Up to date')
      if process_id != feature_type.process_id:
        store_db(session, feature_type, process_id)
      continue

    log.debug('Indexing {} media'.format(mediaCount))

    os.makedirs(fp_feature_path, exist_ok=True)

    # declare the cvmodel here while we actually need it..
    cvmodel = dnn_factory.from_enum(ModelZoo[feature_type.modelzoo_name.upper()])
    
    features = []
    order = []

    medias = session.query(Media).filter(and_(Media.id > process_id, or_(Media.mediaType == 'image', Media.mediaType == 'video_frame'))).order_by('id')

    i = 0
    if hasattr(log, 'progress'):
      log.progress(i, mediaCount, 'Extracting features...')

    for media in medias:
      im = cv.imread(media.fullpath())
      feat_vec = cvmodel.features(im)
      features.append(feat_vec)
      order.append(media.id)
      i += 1
      if i == opt_pagination:
        save_features(session, fp_feature_path, feature_type, features, order)
        store_db(session, feature_type, order[-1])
        features = []
        order = []
        i = 0
        log.progress(i, mediaCount, 'Saving features...')
      elif (i % 100) == 0 and hasattr(log, 'progress'):
        log.progress(i, mediaCount, 'Extracting features...')

    if hasattr(log, 'progress'):
      log.progress(mediaCount, mediaCount, 'Saving features')

    if i > 0:
      save_features(session, fp_feature_path, feature_type, features, order)
      store_db(session, feature_type, order[-1])

def save_features(session, fp_feature_path, feature_type, features, order):
  """Save a 'page' of feature vectors to disk and update the database"""
  now = datetime.datetime.utcnow()
  now = now.replace(tzinfo=pytz.utc)

  min_id = order[0]
  max_id = order[-1]
  tag = "{:09d}_{:09d}".format(min_id, max_id)

  fp_features_out = join(fp_feature_path, tag + '_features.pkl')
  fp_manifest_out = join(fp_feature_path, tag + '_manifest.pkl')

  data = {
    'created': now,
    'model': {
      'name': feature_type.modelzoo_name,
    },
    'order': order,
    'features': features,
  }
  file_utils.write_pickle(data, fp_features_out)

  manifest = {
    'created': now,
    'model': {
      'name': feature_type.modelzoo_name,
    },
    'min_id': min_id,
    'max_id': max_id,
  }
  file_utils.write_pickle(manifest, fp_manifest_out)

def store_db(session, feature_type, process_id, now=None):
  """Update the processed date on the feature type"""
  if now is None:
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)

  feature_type.process_id = process_id
  feature_type.processed_at = now
  session.add(feature_type)
  session.commit()
