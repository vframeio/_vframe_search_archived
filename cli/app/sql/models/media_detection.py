from sqlalchemy import create_engine, Table, Column, String, Integer, Boolean, Text, Index
from sqlalchemy_utc import UtcDateTime, utcnow
import simplejson as json

from app.sql.common import Base

class MediaDetection(Base):
  """Table for referencing feature indexes"""
  __tablename__ = 'feature_type'
  id = Column(Integer, primary_key=True)
  detection_type_id = Column(Integer, ForeignKey('detection_type.id'), nullable=True)
  detection_name_id = Column(Integer, nullable=False)
  media_id = Column(Integer, ForeignKey('media.id'), nullable=True)
  sha256 = Column(HashColumn(32), nullable=False)
  score = Column(Integer, nullable=False)
  w = Column(Integer, nullable=False)
  h = Column(Integer, nullable=False)
  x = Column(Integer, nullable=False)
  y = Column(Integer, nullable=False)

  def toJSON(self):
    return {
      'id': self.id,
    }

# detection_type_name_index = Index('detection_type_name_idx', 'media_detection.detection_type_id', 'media_detection.detection_name_id')
