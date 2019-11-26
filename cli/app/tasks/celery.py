from gevent import monkey
monkey.patch_all()

import simplejson as json 
from app.settings import app_cfg 
from celery import Celery 

celery = Celery(__name__, backend=app_cfg.CELERY_RESULT_BACKEND, broker=app_cfg.CELERY_BROKER_URL) 

from app.tasks.modules.long_task import long_task 
from app.tasks.modules.download_model import download_model
from app.tasks.modules.update_index import update_index

task_classes = {
  'download_model': download_model,
  'long_task': long_task,
  'update_index': update_index,
}

tasks = {
  'download_model': {
    'key': 'download_model',
    'title': 'Download model',
    'params': [ 'name' ],
  },
  'long_task': {  
    'key': 'long_task',
    'title': 'Long task',  
    'params': []
  }, 
  'update_index': {  
    'key': 'update_index',
    'title': 'Update index',  
    'params': []
  }, 
} 
