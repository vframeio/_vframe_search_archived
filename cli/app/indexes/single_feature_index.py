import cv2 as cv

from app.image import cvdnn
from app.models.types import ModelZoo

from app.sql.common import db, Session
from app.sql.models.feature_type import FeatureType
from app.sql.models.media import Media

from app.indexes.index_factory import IndexFactory

class SingleFeatureIndex:
  """Feature vector search that keeps one open model-index pairing at a time."""
  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?
  
  cvmodel = None
  detection_model = None
  index = None
  feature_type = None

  loading = False

  def initialize(self, initial_feature_id=1):
    """Initialize and load the index."""
    session = Session()
    initial_feature = session.query(FeatureType).get(initial_feature_id)
    if initial_feature:
      self.load(initial_feature)
      # load the munitions model, for the time being
      # self.load_detection_model('darknet_yolo_v3_vframe_munitions_v09b')

  def load(self, feature_type):
    """Load a model + index."""
    modelzoo_enum_name = ModelZoo[feature_type.modelzoo_name.upper()]
    print("Loading {}".format(feature_type.modelzoo_name))
    try:
      self.loading = True
      cvmodel = self.dnn_factory.from_enum(modelzoo_enum_name)
      index = IndexFactory(feature_type)
      index.load()

      self.feature_type = feature_type
      self.cvmodel = cvmodel
      self.index = index
    except Exception as e:
      print("Error loading feature index!")
      print(e)
    finally:
      self.loading = False

  def load_detection_model(self, modelzoo_name):
    modelzoo_enum_name = ModelZoo[modelzoo_name.upper()]
    print("Loading {}".format(modelzoo_name))
    try:
      self.loading = True
      detection_model = self.dnn_factory.from_enum(modelzoo_enum_name)
      self.detection_model = detection_model
    except Exception as e:
      print("Error loading feature index!")
      print(e)
    finally:
      self.loading = False

  def query(self, im):
    """Query the index with a filepath, then relate the results back to media records."""
    if self.loading:
      print("Index not ready")
      return []
    feat_vec = self.cvmodel.features(im)
    scores, ids = self.index.query(feat_vec)
    session = Session()
    q = session.query(Media).filter(Media.id.in_(ids))
    medias = q.all()
    return [
      { 'score': float(score), 'media': media.toJSON(), 'id': int(id) }
      for score, media, id in zip(scores, medias, ids)
    ]

  def infer(self, im):
    if self.detection_model is not None:
      results = self.detection_model.infer(im)
    else:
      results = None
    # print(results)
    return(results)
    # for i, classification in enumerate(results.classifications):
    #   txt = f'{(classification.confidence * 100):.2f}% {classification.label}'
    #   im_draw = draw_utils.draw_text(im_draw, (0.1, 0.1*i + 0.1), txt)
