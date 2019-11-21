"""
Add a folder of images / video frames to the database.
"""

import click

@click.command('')
@click.option('-i', '--input', 'opt_dir_in', required=True, 
  help='Path to input image glob directory')
@click.option('--no-check', 'opt_no_check', is_flag=True,
  help='Skip image verification check (tests cv.load before importing, add this flag if your export is already validated)')
@click.pass_context
def cli(ctx, opt_dir_in, opt_no_check):
  """Import a folder of images into the database"""

  import logging

  from app.data.add import add_folder

  log = logging.getLogger('vframe')  # move to ctx

  add_folder(log, opt_dir_in, opt_no_check)
