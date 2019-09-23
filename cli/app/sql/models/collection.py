from sqlalchemy import create_engine, Table, Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utc import UtcDateTime, utcnow
import sqlalchemy.sql.functions as func
from wtforms_alchemy import ModelForm

from app.sql.common import db
from app.sql.models.collection_media import CollectionMedia

class Collection(db.Model):
  """Table for storing references to various media"""
  __tablename__ = 'collection'
  id = Column(Integer, primary_key=True)
  title = Column(String(64, convert_unicode=True), nullable=False)
  username = Column(String(16, convert_unicode=True), nullable=False)
  notes = Column(Text)
  archived = Column(Boolean, default=False)
  created_at = Column(UtcDateTime(), default=utcnow())
  updated_at = Column(UtcDateTime(), onupdate=utcnow())

  medias = relationship("Media", secondary="collection_media")

  def toJSON(self):
    return {
      'id': self.id,
      'title': self.title,
      'username': self.username,
      'notes': self.notes,
      'archived': self.archived,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

  def toFullJSON(self):
    return {
      'id': self.id,
      'title': self.title,
      'username': self.username,
      'notes': self.notes,
      'archived': self.archived,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
      'media': [media.toJSON() for media in self.medias],
    }

def getMediaCounts():
  return db.session.query(
      CollectionMedia.collection_id,
      func.count(CollectionMedia.media_id)
    ).group_by(CollectionMedia.collection_id).all()

class CollectionForm(ModelForm):
  class Meta:
    model = Collection
    exclude = ['created_at', 'updated_at']
