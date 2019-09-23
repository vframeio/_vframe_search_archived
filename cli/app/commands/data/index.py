"""
Rebuild an index of features
"""

import click

from app.data.index import index_features

@click.command('')
@click.pass_context
def cli(ctx):
  """Rebuild an index of features"""

  import logging
  log = logging.getLogger('vframe')  # move to ctx

  index_features(log)
