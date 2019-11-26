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
@click.option('--no-model', 'opt_no_dl_model', is_flag=True)
@click.option('--no-config', 'opt_no_dl_config', is_flag=True)
@click.option('--no-labels', 'opt_no_dl_labels', is_flag=True)
@click.option('--all', 'opt_dl_all', is_flag=True,
  help='Download all models')
@click.option('-f', '--force', 'opt_force', is_flag=True)
@click.pass_context
def cli(ctx, opt_model_enum, opt_no_dl_model, opt_no_dl_config, opt_no_dl_labels, opt_dl_all, opt_force):
  """Download DNN models"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import logging
  from urllib import request
  from pathlib import Path

  from tqdm import tqdm

  from app.settings import app_cfg
  from app.utils import file_utils

  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')

  if opt_model_enum:
    model_list = [opt_model_enum.name.lower()]
  elif opt_all:
    model_list = list(app_cfg.MODELZOO_CFG.keys())
  else:
    log.error('No models selected. Choose "--model" or download "--all"')
    return


  for model_name in tqdm(model_list):

    model_cfg = app_cfg.MODELZOO_CFG.get(model_name)

    dl_files = []
    dl_keys = []

    if not opt_no_dl_model:
      dl_keys.append('model')
    if not opt_no_dl_config:
      dl_keys.append('config')
    if not opt_no_dl_labels:
      dl_keys.append('labels')

    for dl_key in dl_keys:
      fp_out = join(app_cfg.DIR_MODELS, model_cfg.get(dl_key))
      url = join(app_cfg.S3_HTTP_MODELS_URL, model_cfg.get(dl_key))
      if Path(fp_out).is_file() and not opt_force:
        log.debug(f'{fp_out} already exists. Use "-f/--force" to overwrite')
      else:
        dl_files.append({'url': url, 'fp_out': fp_out})


    for dl_file in dl_files:
      log.debug(f'Downloading: {dl_file["url"]} to {dl_file["fp_out"]}')
      file_utils.ensure_dir(dl_file['fp_out'])
      request.urlretrieve(dl_file['url'], dl_file['fp_out'])
