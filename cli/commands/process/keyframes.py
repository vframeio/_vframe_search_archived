import click

@click.command('')
@click.option('-i', '--input', 'opt_dir_in', required=True)
@click.option('-o', '--output', 'opt_dir_out', required=True)
@click.option('-r', '--recursive', 'opt_recursive', is_flag=True)
@click.option('-e', '--ext', 'opt_exts', default=['mp4'], multiple=True, 
  help='Glob ext')
@click.option('--slice', 'opt_slice', type=(int, int), default=(None, None),
  help='Slice list of files')
@click.pass_context
def cli(ctx, opt_dir_in, opt_dir_out, opt_recursive, opt_exts, opt_slice):
  """Converts videos to keyframes using features"""

  # ------------------------------------------------
  # imports

  import os
  from os.path import join
  from glob import glob
  import subprocess

  from tqdm import tqdm
  # import pymediainfo
  
  from app.settings import app_cfg
  from app.utils import log_utils, file_utils

  log = app_cfg.LOG
  log.error('Not yet implemented')
  return