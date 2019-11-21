
# ------------------------------------------------
# imports

import os
from os.path import join
import pickle
import datetime
from pathlib import Path
from glob import glob
from tqdm import tqdm
import shutil

import cv2 as cv

from app.settings import app_cfg
from app.utils import log_utils, file_utils
from app.sql.common import Session, Media

# ------------------------------------------------
# start

def add_folder(log, opt_dir_in, opt_no_check):
  exts = ('png', 'jpg', 'jpeg')
  print(join(opt_dir_in, '**'))
  fp_images = file_utils.glob_exts(opt_dir_in, exts, recursive=True)

  errors = []

  session = Session()

  for fp_image in fp_images:
    fn = os.path.basename(fp_image)

    if '_' in fn:
      mediaType = 'video_frame'
      base, ext = os.path.splitext(fn)
      sha256, frame = base.split('_', 1)
      frame = int(frame)
      imported_im_fn = "{}_{:03d}{}".format(sha256, frame, ext)
    else:
      mediaType = 'image'
      base, ext = os.path.splitext(fn)
      sha256 = file_utils.sha256(fp_image)
      frame = None
      imported_im_fn = "{}{}".format(sha256, ext)

    mediaRecord = {
      'mediaType': mediaType,
      'sha256': sha256,
      'frame': frame,
      'ext': ext,
    }

    imported_im_abspath = join(app_cfg.DIR_MEDIA, file_utils.sha256_tree(sha256))
    imported_im_fullpath = join(imported_im_abspath, imported_im_fn)

    if os.path.exists(imported_im_fullpath):
      errors.append(fp_image)
      print("Already added {}".format(fn))
      continue

    if not opt_no_check:
      try:
        im = cv.imread(fp_image)
      except:
        print("Error reading {}".format(fn))
        errors.append(fp_image)
        continue

    file_utils.ensure_dir(imported_im_abspath)
    shutil.copy(fp_image, imported_im_fullpath)

    media = Media(**mediaRecord)
    session.add(media)
    session.commit()

    # media_feature = MediaFeature(media_id=media.id)
    # session.add(media_feature)
    # session.commit()

  print("Found {} images".format(len(fp_images)))
  print("Added {} images".format(len(fp_images) - len(errors)))
  print("Skipped {} images".format(len(errors)))
