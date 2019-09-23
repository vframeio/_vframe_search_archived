from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey
from sqlalchemy_utc import UtcDateTime, utcnow
from sqlalchemy.orm import relationship
import sqlalchemy.sql.functions as func
from wtforms_alchemy import ModelForm

from app.sql.common import db
from app.sql.models.media import Media

class CollectionMedia(db.Model):
  """Table for storing references to various media"""
  __tablename__ = 'collection_media'
  collection_id = Column(Integer, ForeignKey('collection.id'), primary_key=True)
  media_id = Column(Integer, ForeignKey('media.id'), primary_key=True)
  username = Column(String(16, convert_unicode=True), nullable=False)
  created_at = Column(UtcDateTime(), default=utcnow())

  media = relationship("Media")

  def toJSON(self):
    return {
      'collection_id': self.collection_id,
      'media_id': self.media_id,
      'username': self.username,
      'created_at': self.created_at,
    }

class CollectionMediaForm(ModelForm):
  class Meta:
    model = CollectionMedia
    include = ['collection_id', 'media_id']
    exclude = ['created_at']
