"""Template script
"""

import click

from app.models import types
from app.utils import click_utils

@click.command('')
@click.option('-m', '--model', 'opt_model_enum',
  type=types.ModelZooClickVar,
  required=True,
  help=click_utils.show_help(types.ModelZoo))
@click.pass_context
def cli(ctx, opt_model_enum):
  """Print DNN layer info to find feat vec layer"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import logging
  from urllib import request
  from pathlib import Path

  import numpy as np

  from app.image import cvdnn
  from app.settings import app_cfg
  from app.utils import file_utils

  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')

  log.debug(f'Printing layer info for: {opt_model_enum}')
  dnn_factory = cvdnn.DNNFactory()
  cvmodel = dnn_factory.from_enum(opt_model_enum)
  im = np.zeros([640,480,3],dtype=np.uint8)
  cvmodel._preprocess(im)

  for layer in cvmodel.net.getLayerNames():
    try:
      feat_vec = cvmodel.net.forward(layer)
      log.info(f'{layer}: {feat_vec.shape}')
    except Exception as e:
      log.info(f'{layer}: no features')


  