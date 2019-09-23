import time

from requests import post
import random

from celery.utils.log import get_task_logger
celery_logger = get_task_logger(__name__)

from app.tasks.celery import celery
from app.tasks.log import SocketTaskLog

@celery.task(bind=True)
def long_task(self, uuid, url, params):
  """Background task that runs a long function with progress reports."""
  print(uuid, url, params)
  log = SocketTaskLog(uuid, url)
  verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
  adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
  noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
  message = ''
  total = random.randint(10, 20)
  for i in range(total):
    if not message or random.random() < 0.25:
      message = '{0} {1} {2}...'.format(random.choice(verb),
                                        random.choice(adjective),
                                        random.choice(noun))
    log.progress(i, total, message)
    time.sleep(0.5)

  log.progress(total, total, 'Task completed!')
  log.done()
  return { 'status': 'done' }