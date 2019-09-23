"""Template script
"""

import click

import dacite

from app.models import types
from app.utils import click_utils

actions = ['verify', 'props', 'features', 'infer']

@click.command('')
@click.option('-m', '--model', 'opt_model_enum',
  type=types.ModelZooClickVar,
  help=click_utils.show_help(types.ModelZoo))
@click.option('-a', '--action', 'opt_action', type=click.Choice(actions), default='verify',
  help='Verify action')
@click.option('-i', '--image', 'opt_fp_image', 
  help='Path to image to test classification or features')
@click.pass_context
def cli(ctx, opt_model_enum, opt_action, opt_fp_image):
  """Test ModelZoo models"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import logging
  from pprint import pprint
  
  import numpy as np
  import cv2 as cv

  from app.models.cvmodels import NetConfig
  from app.models.bbox import BBoxNorm
  from app.settings import app_cfg
  from app.image.cvdnn import DNNFactory
  from app.utils import file_utils, draw_utils, display_utils

  # ------------------------------------------------
  # start

  log = logging.getLogger('vframe')  
  errors = []

  log.info(f'Running test "{opt_action}"...')

  dnn_factory = DNNFactory()
  if opt_model_enum:
    model_name = opt_model_enum.name.lower()
    model_cfg = app_cfg.MODELZOO_CFG.get(model_name)
    model_zoo = {model_name: model_cfg}
  else:
    model_zoo = app_cfg.MODELZOO_CFG

  for name, model_cfg in model_zoo.items():
    
    try:
      dnn_cfg = dacite.from_dict(data_class=NetConfig, data=model_cfg)
    except Exception as e:
      log.error(f'Could not parse: {name}, error: {e}')
      errors.append(e)

    if opt_action == 'verify':
      log.info(f"{dnn_cfg.task_type} - {dnn_cfg.framework}: {dnn_cfg.name}") 

    elif opt_action == 'props':
      log.info(f"{dnn_cfg.task_type} - {dnn_cfg.framework}: {dnn_cfg.name}") 
      log.info(dnn_cfg)
      log.info('')

    elif opt_action == 'features' or opt_action == 'infer':

      cvmodel = dnn_factory.from_dnn_cfg(dnn_cfg)
      if opt_fp_image:
        im = cv.imread(opt_fp_image)
        dim = im.shape[:2][::-1]
      else:
        im = np.zeros([100,100,3],dtype=np.uint8)
        log.warn('No image provided. Using blank image.')

      if opt_action == 'features':
        if dnn_cfg.task_type == 'classification':
          feat_vec = cvmodel.features(im)
          if len(feat_vec) != int(dnn_cfg.dimensions):
            log.warn(f'{name} dim: {len(feat_vec)} != {dnn_cfg.dimensions}')
        else:
          log.warn(f'Features not available for task_type "{dnn_cfg.task_type}"')
            
      elif opt_action == 'infer':

        # run inference
        results = cvmodel.infer(im)

        # Draw results
        im_draw = im.copy()
        if results.task_type == 'classification':
          for result in results.classifications:
            log.debug(result)

          for i, classification in enumerate(results.classifications):
            txt = f'{classification.label}'
            im_draw = draw_utils.draw_text(im_draw, (0.1, 0.1*i + 0.1), txt)
        elif results.task_type == 'detection':
          # print results
          for result in results.detections:
            log.debug(result)

          for detection in results.detections:
            txt = f'{(detection.confidence * 100):.2f}% {detection.label}'
            print(txt)
            r = detection.rect
            xyxy = (r.x1, r.y1, r.x2, r.y2)
            if detection.confidence < 0.7:
              color = (0,125,255)
              stroke_weight = 1
            else:
              color = (0,255,0)
              stroke_weight = 2
            bbox = BBoxNorm.from_xyxy(xyxy)
            im_draw = draw_utils.draw_bbox(im_draw, bbox, color=color, stroke_weight=stroke_weight)
            im_draw = draw_utils.draw_text(im_draw, bbox.p1.xy, txt, size=0.5,color=color)

        # show all images here
        cv.imshow('real', im_draw)
        display_utils.handle_keyboard()

  if not errors:
    log.info(f'{app_cfg.UCODE_OK}: tests ran OK.')
  else:
    log.warn(f'{app_cfg.UCODE_NOK} There were {len(errors)}. Try to fix and rerun.')

        