"""Converts models from TF pbtxt format to OpenCV DNN pbtxt format
"""

import click

from app.models import types

opt_types = ['ssd', 'faster_rcnn', 'mask_rcnn']
@click.command('')
@click.option('-i', '--input', 'opt_fp_in', required=True, 
  help='Path to frozen .pb')
@click.option('-o', '--output', 'opt_fp_out', required=True, 
  help='Path to output .pbtxt')
@click.option('-c', '--config', 'opt_fp_config', required=True, 
  help='Path to TF config')
@click.option('-t', '--type', 'opt_type', type=click.Choice(opt_types), required=True,
  help='Type of network')
@click.pass_context
def cli(ctx, opt_fp_in, opt_fp_out, opt_fp_config, opt_type):
  """Creates OpeCV DNN specific graph .pbtxt"""
  
  """
  Config files are located at:
  https://github.com/tensorflow/models/research/object_detection/samples/configs/
  """

  # ------------------------------------------------
  # imports

  from os.path import join
  import json

  from app.utils import log_utils, file_utils

  
  # ------------------------------------------------
  # start

  log = log_utils.Logger.getLogger()

  if opt_type == 'ssd':
    from app.utils.tf.tf_text_graph_ssd import createSSDGraph as graph_factory
  elif opt_type == 'faster_rcnn':
    from app.utils.tf.tf_text_graph_faster_rcnn import createFasterRCNNGraph as graph_factory
  elif opt_type == 'mask_rcnn':
    #from app.utils.tf import tf_text_graph_mask_rcnn
    log.error('Not yet implemented')
    return

  graph_factory(opt_fp_in, opt_fp_config, opt_fp_out)

