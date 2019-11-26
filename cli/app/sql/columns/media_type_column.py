import codecs
from sqlalchemy.types import TypeDecorator, Integer
from sqlalchemy import func
from enum import Enum

from app.models.types import MediaTypeIndex, MediaTypeName

# via https://stackoverflow.com/questions/33923914/python-sqlalchemy-binary-column-type-hex-and-unhex
class MediaTypeColumn(TypeDecorator):
  impl = Integer

  def bind_processor(self, dialect):
    """Return a processor that decodes hex values."""
    def process(value):
      return MediaTypeIndex[value] if value in MediaTypeIndex else 0
    return process

  def result_processor(self, dialect, coltype):
    """Return a processor that encodes hex values."""
    def process(value):
      return MediaTypeName[value]
    return process

  def adapt(self, impltype):
    """Produce an adapted form of this type, given an impl class."""
    return VarBinaryHex()

# class MediaTypeColumn(Integer):
#   def bind_expression(self, bindvalue):
#     # convert the bind's type from String to Enum 
#     return MediaTypeIndex[bindvalue] if bindvalue in MediaTypeIndex else 0

#   def column_expression(self, col):
#     # convert select value from Integer to String
#     return MediaTypeName[col]
