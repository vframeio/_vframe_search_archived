"""Template script
"""

import click

from app.models import types


@click.command('')
@click.pass_context
def cli(ctx):
  """Example template file"""

  # ------------------------------------------------
  # imports

  from os.path import join
  from functools import partial

  from app.utils import log_utils
  
  # ------------------------------------------------
  # start

  log = log_utils.Logger.getLogger()
  log.debug('Template works')
