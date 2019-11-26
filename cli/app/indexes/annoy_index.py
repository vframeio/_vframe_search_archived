"""Annoy index is stored on disk but must be rebuilt completely each time"""

import os
import numpy as np
from annoy import AnnoyIndex

from app.settings import app_cfg

class AnnoyIndex:
  def __init__(self, feature):
    self.feature = feature
    self.model_cfg = app_cfg.MODELZOO_CFG.get(feature.modelzoo_name)
    self.recipe = self.feature.get_recipe('annoy')
    self.dimension = model_cfg.get('dimension')

    if 'metric' not in self.recipe:
      print("No metric specified!")

    self.metric = self.recipe['metric']
    self.n_trees = self.recipe['n_trees']
    
    self.path = os.path.join(app_cfg.DIR_INDEXES, self.feature.index_type, self.feature.modelzoo_name)
    self.fn = path.join(self.path, "annoy-{}-{}.index".format(self.metric, self.n_trees))
    self.can_append = False
    os.makedirs(self.path, exist_ok=True)

  def load(self):
    if os.path.exists(self.fn):
      self.index = AnnoyIndex(self.dimension, self.metric)
      self.index.load(self.fn)
    else:
      return self.create()

  def create(self):
    self.index = AnnoyIndex(self.dimension, self.metric)
    self.count = 0

  def add(self, vecs):
    for vec in vecs:
      self.add_one(vec)

  def add_one(self, vec):
    self.count += 1
    self.index.add_item(self.count, vec)

  def save(self):
    self.index.build(self.n_trees)
    self.index.save(self.fn)

  def query(self, query, offset=0, limit=30):
    end = offset + limit
    indexes, distances = self.index.get_nns_by_vector(query, end, include_distances=True)

    if len(indexes) == 0:
      print("weird, no results!")
      return []

    if offset > 0:
      distances = distances[offset:offset+limit]
      indexes = indexes[offset:offset+limit]

    if len(indexes) == 0:
      print("no results!")
      return []

    return distances, indexes
