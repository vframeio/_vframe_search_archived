import os
from os.path import join
import collections
from dotenv import load_dotenv

import yaml

from app.models import types
from pathlib import Path

import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

# -----------------------------------------------------------------------------
# .env config for keys
# -----------------------------------------------------------------------------

# DIR_DOTENV = join(DIR_APP, '.env')
load_dotenv() # dotenv_path=DIR_DOTENV)
PRODUCTION = os.getenv('ENV') == 'production'

# -----------------------------------------------------------------------------
# File I/O
# -----------------------------------------------------------------------------

SELF_CWD = os.path.dirname(os.path.realpath(__file__))  # Script CWD
DIR_VFRAME_SEARCH = str(Path(SELF_CWD).parent.parent.parent)

DIR_DATA_STORE = join(DIR_VFRAME_SEARCH, 'data_store')

DIR_MEDIA = join(DIR_DATA_STORE, 'media')
DIR_UPLOADS = join(DIR_DATA_STORE, 'uploads')
DIR_MODELS = join(DIR_DATA_STORE, 'models')
DIR_FEATURES = join(DIR_DATA_STORE, 'features')
DIR_INDEXES = join(DIR_DATA_STORE, 'indexes')
DIR_EXPORTS = join(DIR_DATA_STORE, 'exports')

DIR_DOCS = join(DIR_VFRAME_SEARCH, 'docs')
DIR_MODELZOO = join(DIR_VFRAME_SEARCH, 'modelzoo')
FP_MODELZOO = join(DIR_VFRAME_SEARCH, 'modelzoo/modelzoo.yaml')

URL_DATA = '/static/data/'
URL_MEDIA = join(URL_DATA, 'media')
URL_UPLOADS = join(URL_DATA, 'uploads')
URL_EXPORTS = join(URL_DATA, 'exports')

if 'cli' in os.getcwd():
  DIR_STATIC = os.path.abspath('../static')
else:
  DIR_STATIC = os.path.abspath('static')

# -----------------------------------------------------------------------------
# Model config
# -----------------------------------------------------------------------------

with open(FP_MODELZOO, 'r') as fp:
  MODELZOO_CFG = yaml.load(fp, Loader=yaml.Loader)

# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
SOCKETIO_MESSAGE_QUEUE = os.getenv('SOCKETIO_MESSAGE_QUEUE') or 'redis://localhost:6379/0'

# -----------------------------------------------------------------------------
# S3 storage
# -----------------------------------------------------------------------------

S3_HTTP_BASE_URL = 'https://vframe.ams3.digitaloceanspaces.com/v2/'
S3_HTTP_MODELS_URL = join(S3_HTTP_BASE_URL, 'models')
DIR_S3 = 'v2'
DIR_S3_MODELS = join(DIR_S3, 'models')


# -----------------------------------------------------------------------------
# Unicode symbols for logger
# -----------------------------------------------------------------------------

UCODE_OK = u"\u2714"  # check ok
UCODE_NOK = u'\u2718'  # x no ok