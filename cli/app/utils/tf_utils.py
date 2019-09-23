"""
TensorFlow utility scripts
- convert models and labels
"""

import json

def tf_pbtxt_labelmap_to_json(fp_pbtxt):
  '''Converts TensorFlow pbtxt label map to JSON
  :param fp_txt: filepath to pbtxt
  '''
  with open(fp_pbtxt, 'r') as fp:
    txt = fp.readlines()
  items = [txt[(i*5):((i+1)*5)] for i in range(0, len(txt)//5)]
  mapped_labels = []
  for item in items:
    item[0] = item[0].replace('item','')
    item[1] = item[1].replace('\n', ',').replace('name', '"name"')
    item[2] = item[2].replace('\n', ',').replace('id', '"id"')
    item[3] = item[3].replace('display_name', '"display_name"')
    item = ''.join(item)
    item = item.replace('\n', '')
    j = json.loads(item)
    mapped_labels.append(j)
  return mapped_labels