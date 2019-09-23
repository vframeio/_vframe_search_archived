"""
Extract a feature from the images in the database
"""

import click

@click.command('')
# @click.option('-m', '--model', 'opt_model_enum',
#   default=click_utils.get_default(types.ModelZoo.CAFFE_BVLC_GOOGLENET_IMAGENET),
#   type=types.ModelZooClickVar,
#   show_default=True,
#   help=click_utils.show_help(types.ModelZoo))
@click.option('-p', '--pagination', 'opt_pagination', type=int, default=50000, help='Max IDs per page of results')
@click.pass_context
def cli(ctx, opt_pagination):
  """Extract features from the images in the database"""

  import logging
  from app.data.extract import extract_features
  
  log = logging.getLogger('vframe')  # move to ctx

  extract_features(log, opt_pagination)
