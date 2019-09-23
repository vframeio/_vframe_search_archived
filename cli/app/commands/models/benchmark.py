import click

import dacite

from app.models import types
from app.utils import click_utils

@click.command('')
@click.pass_context
def cli(ctx,):
  """TODO Benchmark model inference FPS and update YAML"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import logging
  
  import numpy as np

  from app.models.cvmodels import NetConfig
  from app.settings import app_cfg
  from app.image.cvdnn import DNNFactory

  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')
  errors = []

  log.info(f'Running test "{opt_action}"...')

  dnn_factory = DNNFactory()

  for name, model_cfg in app_cfg.MODELZOO_CFG.items():
    
    try:
      dnn_cfg = dacite.from_dict(data_class=NetConfig, data=model_cfg)
    except Exception as e:
      log.error(f'Could not parse: {name}, error: {e}')
      errors.append(e)
