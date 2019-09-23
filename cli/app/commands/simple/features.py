"""
Extract features from a folder of images and write them to a pickle
"""

import click

from app.models import types
from app.utils import click_utils

@click.command('')
@click.option('-i', '--input', 'opt_dir_in', required=True, 
  help='Path to input image glob directory')
@click.option('-o', '--output', 'opt_fp_out', required=True,
  help='Path to output .pkl file')
@click.option('-m', '--model', 'opt_model_enum',
  default=click_utils.get_default(types.ModelZoo.CAFFE_BVLC_GOOGLENET_IMAGENET),
  type=types.ModelZooClickVar,
  show_default=True,
  help=click_utils.show_help(types.ModelZoo))
@click.pass_context
def cli(ctx, opt_dir_in, opt_fp_out, opt_model_enum):
  """Converts directory of images to feature vectors"""

  # ------------------------------------------------
  # imports

  import os
  import pickle
  import datetime
  import logging
  from os.path import join
  from glob import glob
  from tqdm import tqdm

  import cv2 as cv

  from app.settings import app_cfg
  from app.utils import log_utils, file_utils

  from app.image import cvdnn
  
  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')  # move to ctx

  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?
  cvmodel = dnn_factory.from_enum(opt_model_enum)

  exts = ('png', 'jpg', 'jpeg')
  fp_images = file_utils.glob_exts(opt_dir_in, exts)

  features = []
  mediaRecords = []

  if hasattr(cvmodel.dnn_cfg, 'features'):
    log.debug(f'Using model: {opt_model_enum} and layer: {cvmodel.dnn_cfg.features}')
  else:
    log.debug(f'Using model: {opt_model_enum}')
  for fp_image in tqdm(fp_images):
    im = cv.imread(fp_image)
    feat_vec = cvmodel.features(im)
    fn = os.path.basename(fp_image)

    if '_' in fn:
      mediaType = 'video_frame'
      base, ext = os.path.splitext(fn)
      sha256, frame = base.split('_', 1)
    else:
      mediaType = 'image'
      sha256 = file_utils.sha256(fp_image)
      frame = -1

    mediaRecord = {
      'mediaType': mediaType,
      'sha256': sha256,
      'frame': frame,
      'url': '/static/data/{}/{}'.format('keyframes', fn),
    }

    mediaRecords.append(mediaRecord)
    features.append(feat_vec)

  data = {
    'created': datetime.datetime.now(),
    'model': {
      'enum': opt_model_enum,
    },
    'mediaRecords': mediaRecords,
    'features': features,
  }
  file_utils.write_pickle(data, opt_fp_out)
