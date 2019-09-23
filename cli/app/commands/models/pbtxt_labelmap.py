"""Converts the labe map .pbtxt files
Custom text replacement used instead of the TF pbtxt parser because
using TF to do this requires installing the whole object detection library
"""

import click

from app.models import types


@click.command('')
@click.option('-i', '--input', 'opt_fp_in', required=True,
  help='Path to label map .pbtxt')
@click.option('-o', '--output', 'opt_fp_out', required=True,
  help='Path to output txt file')
@click.pass_context
def cli(ctx, opt_fp_in, opt_fp_out):
  """Convert TF pbtxt label map to label lines txt"""

  # ------------------------------------------------
  # imports

  from os.path import join
  import json

  from app.utils import log_utils, file_utils
  
  # ------------------------------------------------
  # start

  log = log_utils.Logger.getLogger()


  def tf_pbtxt_labelmap_to_json(fp_pbtxt):
    '''Converts TensorFlow pbtxt label map to JSON
    :param fp_txt: filepath to pbtxt
    :returns: [list] of [dict]
    '''
    with open(fp_pbtxt, 'r') as fp:
      txt = fp.readlines()
    items = [txt[(i*5):((i+1)*5)] for i in range(0, len(txt)//5)]
    mapped_labels = []
    for item in items:
      # parse items and convert to a JSON dict
      item[0] = item[0].replace('item','')
      item[1] = item[1].replace('\n', ',').replace('name', '"name"')
      item[2] = item[2].replace('\n', ',').replace('id', '"id"')
      item[3] = item[3].replace('display_name', '"display_name"')
      item = ''.join(item)
      item = item.replace('\n', '')
      j = json.loads(item)
      mapped_labels.append(j)
    return mapped_labels

  mapped_labels = tf_pbtxt_labelmap_to_json(opt_fp_in)
  labels = [x['display_name'] for x in mapped_labels]
  file_utils.write_text(labels, opt_fp_out)



