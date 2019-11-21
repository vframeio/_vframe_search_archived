import click

@click.command('')
@click.option('-i', '--input', 'opt_dir_in', required=True)
@click.option('-o', '--output', 'opt_dir_out', required=True)
@click.option('-r', '--recursive', 'opt_recursive', is_flag=True)
@click.option('-e', '--ext', 'opt_exts', default=['mp4'], multiple=True, 
  help='Glob ext')
@click.option('--slice', 'opt_slice', type=(int, int), default=(None, None),
  help='Slice list of files')
@click.option('-t', '--threshold', 'opt_threshold', default=0.3,
  help='FFMPEG scene threshold')
@click.option('--size', 'opt_size', default=(960,540), help='Max size')
@click.pass_context
def cli(ctx, opt_dir_in, opt_dir_out, opt_recursive, opt_exts, opt_threshold,
  opt_slice, opt_size):
  """Converts videos to keyframes using FFMPEG"""

  # ------------------------------------------------
  # imports

  import os
  from os.path import join
  from glob import glob
  import subprocess

  from tqdm import tqdm
  
  from app.settings import app_cfg
  from app.utils import log_utils, file_utils, video_utils

  log = app_cfg.LOG
  log.info(f'opt_exts: {opt_exts}')

  fp_videos = file_utils.glob_exts(opt_dir_in, opt_exts, recursive=opt_recursive)
  if any(opt_slice):
    fp_videos = fp_videos[opt_slice[0]:opt_slice[1]]

  log.info(f'Processing: {len(fp_videos):,} videos')

  for fp_video in tqdm(fp_videos):
    
    # get sizes for resize
    meta = video_utils.mediainfo(fp_video)
    scale = max(meta['width']/opt_size[0], meta['height']/opt_size[1])
    w,h = ((int(meta['width']//scale)), int((meta['height']//scale)))
    log.debug(f'scale: {scale}, orig: {meta["width"]} {meta["height"]} w,h: {w} {h}')
    cmd_ss = f"select='gt(scene,{opt_threshold})', scale={w}:{h}"
    
    # create filename
    sha256 = file_utils.sha256(fp_video)  # use sha256 as filename
    fn = f'{sha256}_%03d.jpg'  # max 3 zero padding
    fp_out = join(opt_dir_out, sha256, fn)
    file_utils.mkdirs(fp_out)

    # run FFMPEG
    cmd = ['ffmpeg', '-i', fp_video, 
      '-vf', cmd_ss,  # video filter
      '-qscale:v', '2',   # quality
      '-vsync', 'vfr',   # ?
      fp_out]
    subprocess.call(cmd)
