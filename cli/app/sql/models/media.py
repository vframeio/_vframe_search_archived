from sqlalchemy import create_engine, Table, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utc import UtcDateTime, utcnow
import sqlalchemy.sql.functions as func
from wtforms_alchemy import ModelForm

from app.sql.common import db
from app.sql.columns.hash_column import HashColumn
from app.sql.columns.media_type_column import MediaTypeColumn
from app.models.types import MediaTypeIndex, MediaTypeName

from app.utils.file_utils import sha256_tree
from app.settings import app_cfg

from os.path import join

class Media(db.Model):
  """Table for storing references to various media"""
  __tablename__ = 'media'
  id = Column(Integer, primary_key=True)
  # parent_id = Column(Integer, ForeignKey('media.id'), nullable=True)
  mediaType = Column(MediaTypeColumn(), nullable=False)
  sha256 = Column(HashColumn(32), nullable=False)
  ext = Column(String(4, convert_unicode=True), nullable=False)
  frame = Column(Integer, nullable=True)
  created_at = Column(UtcDateTime(), default=utcnow())

  # children = relationship("Media")
  media_features = relationship("MediaFeature")
  media_metadata = relationship("MediaMetadata")

  def toJSON(self):
    return {
      'id': self.id,
      # 'parent_id': self.parent_id,
      'mediaType': self.mediaType,
      'sha256': self.sha256,
      'frame': self.frame,
      'ext': self.ext,
      'url': self.url(),
      'created_at': self.created_at,
    }

  def toFullJSON(self):
    siblings = db.session.query(Media).filter(Media.sha256 == self.sha256).all()
    return {
      'el': self.toJSON(),
      'siblings': [ el.toJSON() for el in siblings ],
    }

  def filename(self):
    if self.mediaType == 'video_frame':
      return "{}_{:03d}{}".format(self.sha256, self.frame, self.ext)
    return "{}{}".format(self.sha256, self.ext)

  def filetree(self):
    return sha256_tree(self.sha256)

  def filepath(self):
    return join(app_cfg.DIR_MEDIA, self.filetree())

  def fullpath(self):
    return join(self.filepath(), self.filename())

  def archivepath(self):
    return join('media', self.filename())

  def url(self):
    return join(app_cfg.URL_MEDIA, self.filetree(), self.filename())
