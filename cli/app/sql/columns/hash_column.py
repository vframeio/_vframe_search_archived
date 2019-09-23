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

# def process_bind_param(self, value, dialect):
#   # encode value as a binary
#   if value:
#     return bytes(value, 'utf-8')

# def bind_expression(self, bindvalue):
#   # convert the bind's type from String to HEX encoded 
#   return func.HEX(bindvalue)

# def column_expression(self, col):
#   # convert select value from HEX encoded to String
#   return func.UNHEX(col)
