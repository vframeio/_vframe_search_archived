"""Sync models to S3 Spaces
"""

import click

from app.models import types
from app.utils import click_utils

@click.command('')
@click.option('-m', '--model', 'opt_model_enum',
  type=types.ModelZooClickVar,
  help=click_utils.show_help(types.ModelZoo))
@click.option('--all', 'opt_all', is_flag=True,
  help='Sync all models')
@click.option('--list', 'opt_list', is_flag=True,
  help='List models and exit')
@click.pass_context
def cli(ctx, opt_model_enum, opt_all, opt_list):
  """Sync models to S3 storage"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import logging
  from pathlib import Path

  from tqdm import tqdm

  from app.utils import s3_utils
  from app.settings import app_cfg

  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')  

  # init s3 api
  s3 = s3_utils.RemoteStorageS3()

  if opt_model_enum:
    model_list = [opt_model_enum.name.lower()]
  elif opt_all:
    model_list = list(app_cfg.MODELZOO_CFG.keys())
  elif opt_list:
    s3.list_dir(app_cfg.DIR_S3_MODELS)
    return
  else:
    log.error('No models selected. Choose "--model" or sync "--all"')
    return

  for model_name in tqdm(model_list):
    
    model_cfg = app_cfg.MODELZOO_CFG.get(model_name)

    if model_cfg.get('active'):
      log.debug(f'Syncing model: {model_name}')
      
      # sync model dir
      if model_cfg.get('model'):
        model_path = model_cfg.get('model')
        fp_local = Path(join(app_cfg.DIR_MODELS, model_path))
        if fp_local.is_file():
          dir_local_model = str(fp_local.parent)
          dir_remote = str(Path(join(app_cfg.DIR_S3_MODELS, model_path)).parent)
          log.debug(f'Sync: {dir_local_model} --> {dir_remote}')
          s3.sync_dir(dir_local_model, dir_remote)
        else:
          log.warn(f'No file exists locall: {fp_local}')
          dir_model = ''
      else:
        log.warn(f'no config file')

      # sync config dir if not model
      if model_cfg.get('config'):
        cfg_path = model_cfg.get('config')
        fp_local = Path(join(app_cfg.DIR_MODELS, cfg_path))
        if fp_local.is_file():
          dir_local_config = str(fp_local.parent)
          if dir_local_config != dir_local_model:
            dir_remote = str(Path(join(app_cfg.DIR_S3_MODELS, cfg_path)).parent)
            log.debug(f'Sync: {dir_local_labels} --> {dir_remote}')
            s3.sync_dir(dir_local_labels, dir_remote)
        else:
          log.warn(f'No file exists locally: {fp_local}')
          dir_config = ''

      # sync labels dir if not config or models
      if model_cfg.get('labels'):
        cfg_path = model_cfg.get('labels')
        fp_local = Path(join(app_cfg.DIR_MODELS, cfg_path))
        if fp_local.is_file():
          dir_local_labels = str(fp_local.parent)
          if dir_local_labels != dir_local_model and dir_local_labels != dir_local_config:
            dir_remote = str(Path(join(app_cfg.DIR_S3_MODELS, cfg_path)).parent)
            log.debug(f'Sync: {dir_local_labels} --> {dir_remote}')
            s3.sync_dir(dir_local_labels, dir_remote)
      else:
        log.debug(f'Skipping labels for {model_name}')
