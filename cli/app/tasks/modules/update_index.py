import time

from requests import post
import random

from celery.utils.log import get_task_logger
celery_logger = get_task_logger(__name__)

from app.tasks.celery import celery
from app.tasks.log import SocketTaskLog

from app.data.extract import extract_features
from app.data.index import index_features

@celery.task(bind=True)
def update_index(self, uuid, url, params):
  """Task which will update the index."""
  log = SocketTaskLog(uuid, url)

  extract_features(log)
  index_features(log)
  
  log.done()
  return { 'status': 'done' }