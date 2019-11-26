"""FAISS index can use PCA to reduce file size but runs in-memory"""

import os
import numpy as np
import faiss

from app.settings import app_cfg

class FAISSIndex:
  def __init__(self, feature):
    self.feature = feature
    self.model_cfg = app_cfg.MODELZOO_CFG.get(feature.modelzoo_name)
    self.recipe = self.feature.get_recipe('faiss')

    if 'factory_type' not in self.recipe:
      print("No factory_type specified!")

    self.factory_type = self.recipe['factory_type']

    self.path = os.path.join(app_cfg.DIR_INDEXES, self.feature.index_type, self.feature.modelzoo_name)
    self.fn = path.join(self.path, "faiss-{}.index".format(self.factory_type.replace(',', '_')))
    self.can_append = True
    os.makedirs(self.path, exist_ok=True)

  def load(self):
    if os.path.exists(self.fn):
      self.index = faiss.read_index(self.fn)
    else:
      return self.create()

  def create(self):
    self.index = faiss.index_factory(model_cfg.get('dimension'), self.factory_type)

  def train(self, vecs):
    '''Optional FAISS-only pretraining step'''
    vecs = np.array(vecs)
    index.train(vecs)

  def add(self, vecs):
    vecs = np.array(vecs)
    self.index.add(vecs)

  def add_one(self, vec):
    self.index.add([vec])

  def save(self):
    faiss.write_index(self.index, self.fn)

  def query(self, query, offset=0, limit=30):
    end = offset + limit
    distances, indexes = self.index.search(query, end)

    if len(indexes) == 0:
      print("weird, no results!")
      return []

    distances = distances[0]
    indexes = indexes[0]

    if offset > 0:
      distances = distances[offset:offset+limit]
      indexes = indexes[offset:offset+limit]

    if len(indexes) == 0:
      print("no results!")
      return []

    return distances, indexes


# add_start = time.time()
# index.add(feats)
# add_end = time.time()
# add_time = add_end - add_start
