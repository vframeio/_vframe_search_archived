from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey
import sqlalchemy.sql.functions as func

from app.sql.common import db

class MediaFeature(db.Model):
  """Table for storing feature vectors pertaining to media"""
  __tablename__ = 'media_feature'
  id = Column(Integer, primary_key=True)
  media_id = Column(Integer, ForeignKey('media.id'), nullable=False)

  def toJSON(self):
    return {
      'id': self.id,
      'media_id': self.media_id,
    }
