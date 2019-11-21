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

  import logging
  from pathlib import Path
  from os.path import join

  from tqdm import tqdm
  import cv2 as cv

  from app.image import cvdnn
  from app.utils import file_utils
  
  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')  # move to ctx

  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?
  cvmodel = dnn_factory.from_enum(opt_model_enum)

  exts = ('png', 'jpg', 'jpeg')
  fp_images = file_utils.glob_exts(opt_dir_in, exts)

  feats = []
  fns = []

  log.debug(f'Using model: {opt_model_enum} and layer: {cvmodel.dnn_cfg.features}')
  for fp_image in tqdm(fp_images):
    im = cv.imread(fp_image)
    feat_vec = cvmodel.features(im)
    fns.append(str(Path(fp_image).name))
    feats.append(feat_vec)

  data = {
    'fns': fns,
    'feats': feats,
  }
  file_utils.write_pickle(data, opt_fp_out)