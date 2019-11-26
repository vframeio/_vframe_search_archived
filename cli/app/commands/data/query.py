"""
Query an index with a feature
"""

import click

import datetime
import pytz
from os.path import join

from app.models import types
from app.utils import click_utils, file_utils

@click.command('')
# @click.option('-m', '--model', 'opt_model_enum',
#   default=click_utils.get_default(types.ModelZoo.CAFFE_BVLC_GOOGLENET_IMAGENET),
#   type=types.ModelZooClickVar,
#   show_default=True,
#   help=click_utils.show_help(types.ModelZoo))
# @click.option('-p', '--pagination', 'opt_pagination', type=int, default=50000, help='Max IDs per page of results')
@click.pass_context
def cli(ctx):
  """Query an index with a feature"""

  # ------------------------------------------------
  # imports

  import os
  import pickle
  import logging
  from glob import glob
  from tqdm import tqdm

  import cv2 as cv
  from sqlalchemy import or_, and_
  from sqlalchemy_utc import utcnow
  from sqlalchemy import func
  from werkzeug.utils import secure_filename

  from app.settings import app_cfg
  from app.models.types import MediaType, ModelZoo
  from app.utils import log_utils, file_utils
  from app.sql.common import db, Session

  from app.image import cvdnn

  from app.sql.models.feature_type import FeatureType
  from app.sql.models.media import Media
  from app.sql.models.upload import Upload
  from app.indexes.index_factory import IndexFactory
  from app.models.types import ModelZoo

  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?

  session = Session()

  feature_type = session.query(FeatureType).get(1)

  modelzoo_enum_name = ModelZoo[feature_type.modelzoo_name.upper()]

  print("Loading {}".format(feature_type.modelzoo_name))

  cvmodel = dnn_factory.from_enum(modelzoo_enum_name)

  print("Loading index")

  index = IndexFactory(feature_type)
  index.load()

  print("Querying image")

  media = session.query(Media).get(1)
  path = media.fullpath()

  im = cv.imread(path)
  feat_vec = cvmodel.features(im)
  scores, ids = index.query(feat_vec)

  print("Looking up results")

  q = session.query(Media).filter(Media.id.in_(ids))

  medias = q.all()
  # media_lookup = { media.id: media for media in medias }

  for media in medias:
    print(media.fullpath())
