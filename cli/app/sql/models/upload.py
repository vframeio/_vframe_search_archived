from sqlalchemy import create_engine, Table, Column, String, Integer, DateTime
import sqlalchemy.sql.functions as func
from sqlalchemy_utc import UtcDateTime, utcnow
from wtforms_alchemy import ModelForm

from app.sql.common import db
from app.sql.columns.hash_column import HashColumn
from app.sql.columns.media_type_column import MediaTypeColumn

from app.utils.file_utils import sha256_tree
from app.settings import app_cfg

from os.path import join

class Upload(db.Model):
  """Table for storing references to various media"""
  __tablename__ = 'uploads'
  id = Column(Integer, primary_key=True)
  sha256 = Column(HashColumn(32), nullable=False)
  ext = Column(String(4, convert_unicode=True), nullable=False)
  username = Column(String(16, convert_unicode=True), nullable=False)
  created_at = Column(UtcDateTime(), default=utcnow())

  def toJSON(self):
    return {
      'id': self.id,
      'sha256': self.sha256,
      'ext': self.ext,
      'username': self.username,
      'url': self.url(),
      'created_at': self.created_at,
    }

  def filename(self):
    return "{}{}".format(self.sha256, self.ext)

  def filepath(self):
    return join(app_cfg.DIR_UPLOADS, sha256_tree(self.sha256))

  def fullpath(self):
    return join(self.filepath(), self.filename())

  def url(self):
    return join(app_cfg.URL_UPLOADS, sha256_tree(self.sha256), self.filename())
