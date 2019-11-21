import codecs
from sqlalchemy.types import TypeDecorator, VARBINARY
from sqlalchemy import func

# via https://stackoverflow.com/questions/33923914/python-sqlalchemy-binary-column-type-hex-and-unhex
class HashColumn(TypeDecorator):
  impl = VARBINARY

  def bind_processor(self, dialect):
    """Return a processor that decodes hex values."""
    def process(value):
      return codecs.decode(value, 'hex')
    return process

  def result_processor(self, dialect, coltype):
    """Return a processor that encodes hex values."""
    def process(value):
      return codecs.encode(value, 'hex').decode('utf-8')
    return process

  def adapt(self, impltype):
    """Produce an adapted form of this type, given an impl class."""
    return VarBinaryHex()
