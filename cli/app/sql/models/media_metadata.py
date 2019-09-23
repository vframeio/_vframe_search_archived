from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey
import sqlalchemy.sql.functions as func

from app.sql.common import db

class MediaMetadata(db.Model):
  """Table for media metadata (usually URLs but possibly JSON?)"""
  __tablename__ = 'media_metadata'
  
  id = Column(Integer, primary_key=True)
  media_id = Column(Integer, ForeignKey('media.id'), nullable=False)
  url = Column(String(256, convert_unicode=True), nullable=False)

  def toJSON(self):
    return {
      'id': self.id,
      'media_id': self.media_id,
      'url': self.url,
    }
