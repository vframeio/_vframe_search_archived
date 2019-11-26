"""
Rebuild an index of features
"""

import os
import logging
import datetime
import pytz
from glob import glob
from os.path import join

import cv2 as cv
from sqlalchemy import or_, and_
from sqlalchemy_utc import utcnow
from werkzeug.utils import secure_filename

from app.settings import app_cfg
from app.models.types import MediaType, ModelZoo
from app.utils import log_utils, file_utils
from app.indexes.index_factory import IndexFactory
from app.sql.common import Session, Media, FeatureType, db

from app.image import cvdnn

def index_features(log):
  session = Session()

  feature_types = session.query(FeatureType).filter(FeatureType.active == True).all()

  if hasattr(log, 'progress'):
    log.progress(0, len(feature_types), 'Indexing...')

  for i, feature_type in enumerate(feature_types):
    index = IndexFactory(feature_type)

    fp_feature_path = join(app_cfg.DIR_FEATURES, feature_type.modelzoo_name)
    fp_feature_pkls = sorted(glob(join(fp_feature_path, '*_features.pkl')))

    # if not index.can_append:
    index.create()

    max_id = 0

    # log.debug(fp_feature_pkls)
  
    for fp_feature_pkl in fp_feature_pkls:
      fp_manifest_pkl = fp_feature_pkl.replace('_features.pkl', '_manifest.pkl')
      manifest = file_utils.load_pickle(fp_manifest_pkl)
      max_id = manifest['max_id']

      features = file_utils.load_pickle(fp_feature_pkl)
      index.add(features['features'])

    index.save()

    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)

    feature_type.index_id = max_id
    feature_type.indexed_at = now
    session.add(feature_type)
    session.commit()
 
    if hasattr(log, 'progress'):
      log.progress(i, len(feature_types), 'Indexing...')

  if hasattr(log, 'progress'):
    log.progress(len(feature_types), len(feature_types), 'Done')
