from sqlalchemy import create_engine, Table, Column, String, Integer, Boolean, Text
from sqlalchemy_utc import UtcDateTime, utcnow
from wtforms_alchemy import ModelForm
import simplejson as json

from app.sql.common import Base

class DetectionType(Base):
  """Table for referencing feature indexes"""
  __tablename__ = 'feature_type'
  id = Column(Integer, primary_key=True)
  active = Column(Boolean, default=True)
  modelzoo_name = Column(String(64, convert_unicode=True), nullable=False, unique=True)
  username = Column(String(16, convert_unicode=True))
  created_at = Column(UtcDateTime(), default=utcnow())
  updated_at = Column(UtcDateTime(), onupdate=utcnow())
  process_id = Column(Integer, default=0)
  processed_at = Column(UtcDateTime(), nullable=True)
  index_id = Column(Integer, default=0)
  indexed_at = Column(UtcDateTime(), nullable=True)
  index_settings = Column(Text, nullable=True)

  def toJSON(self):
    return {
      'id': self.id,
      'active': self.active,
      'modelzoo_name': self.modelzoo_name,
      'username': self.username,
      'created_at': self.created_at,
      'processed_at': self.processed_at,
      'process_id': self.process_id,
      'indexed_at': self.indexed_at,
      'index_id': self.index_id,
      'index_settings': self.index_settings, # a JSON blob with e.g. factory type
    }

  def get_recipe(self, type):
    try:
      data = json.loads(self.index_settings)
    except Exception as e:
      print(e)
      return {}
    if type in data:
      return data[type]
    return {}

class FeatureTypeForm(ModelForm):
  class Meta:
    model = FeatureType
    exclude = ['created_at', 'indexed_at', 'processed_at', 'process_id', 'index_id', 'index_settings']
