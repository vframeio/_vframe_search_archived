import time

from app.models import types

from app.tasks.celery import celery

@celery.task(bind=True)
def download_model(self, uuid, url, params):

  # ------------------------------------------------
  # imports

  from os.path import join
  from urllib import request
  from pathlib import Path

  from app.settings import app_cfg
  from app.utils import file_utils
  from app.models.types import ModelZoo
  from app.tasks.log import SocketTaskLog

  # ------------------------------------------------
  # start

  log = SocketTaskLog(uuid, url)
  name = params['name']

  if name == 'all':
    model_list = list(app_cfg.MODELZOO_CFG.keys())
  else:
    names = set(item.name for item in ModelZoo)
    if name.upper() not in names:
      log.error("Model not found in model zoo")
      log.done()
      return
    else:
      model_list = [name]

  dl_files = []

  for model_name in model_list:

    model_cfg = app_cfg.MODELZOO_CFG.get(model_name)

    dl_keys = ['labels', 'config', 'model']

    for dl_key in dl_keys:
      fp_out = join(app_cfg.DIR_MODELS, model_cfg.get(dl_key))
      url = join(app_cfg.S3_HTTP_MODELS_URL, model_cfg.get(dl_key))
      if Path(fp_out).is_file():
        # log.debug(f'{fp_out} already exists.')
        pass
      else:
        dl_files.append({'url': url, 'fp_out': fp_out})

  log.progress(0, len(dl_files), 'Starting download...')

  for i, dl_file in enumerate(dl_files):
    log.debug(f'Downloading: {dl_file["url"]} to {dl_file["fp_out"]}')
    file_utils.ensure_dir(dl_file['fp_out'])
    try:
      request.urlretrieve(dl_file['url'], dl_file['fp_out'])
      log.progress(i, len(dl_files), "Downloading " + model_name)
    except Exception as e:
      log.error('Problem fetching url ' + url)
      log.done()

  log.progress(len(dl_files), len(dl_files), 'Download complete')
  log.done()
