"""Flat index is a pickle file of feature vectors, loaded into memory"""

import os
import numpy as np

from app.settings import app_cfg
from app.models.types import MediaType, ModelZoo
from app.utils import log_utils, file_utils

class FlatIndex:
  def __init__(self, feature):
    self.feature = feature
    self.path = os.path.join(app_cfg.DIR_INDEXES, self.feature.index_type, self.feature.modelzoo_name)
    self.fn = os.path.join(self.path, 'flat.pkl')
    self.can_append = True
    os.makedirs(self.path, exist_ok=True)

  def load(self):
    if os.path.exists(self.fn):
      self.index = file_utils.load_pickle(self.fn)
      print("Loaded {} vectors".format(len(self.index)))
    else:
      self.create()

  def create(self):
    self.index = []

  def add(self, vecs):
    self.index += vecs

  def add_one(self, vec):
    self.index.append(vec)

  def save(self):
    file_utils.write_pickle(self.index, self.fn)

  def query(self, query, offset=0, limit=30):
    dists = np.linalg.norm(self.index - query, axis=1)
    start = offset
    end = offset + limit
    ids = np.argsort(dists)[start:end]

    scores = [ dists[id] for id in ids ]

    return scores, list([int(id+1) for id in ids])  # sql ids start at 1
