"""Template script
"""

import click

@click.command('')
@click.pass_context
def cli(ctx):
  """Example template file"""

  # ------------------------------------------------
  # imports

  import logging
  
  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')
  log.debug('Template works')
