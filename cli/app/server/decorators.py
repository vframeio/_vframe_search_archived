import os
from time import time
from datetime import datetime
import numpy as np
import cv2 as cv
from flask import request, jsonify
from werkzeug.utils import secure_filename

from app.sql.common import Session

DEFAULT_LIMIT = 30

def api_query(f):
  """Wrap basic API queries that use offset/limit parameters"""
  def wrap_api_query(*args, **kwargs):
    start = time()
    query = {}
    kwargs['query'] = query
    results = f(*args, **kwargs)
    query['timing'] = round(time() - start, 2)
    if isinstance(results, list):
      return { 'query': query, 'results': results }
    else:
      return { 'query': query, 'result': results }
  wrap_api_query.__name__ = f.__name__
  return wrap_api_query

def db_session(f):
  """Wrap API queries in a database session object which gets committed"""
  def wrap_db_session(*args, **kwargs):
    session = Session()
    try:
      kwargs['session'] = session
      f(*args, **kwargs)
      session.commit()
    except:
      session.rollback()
      raise
    finally:
      session.close()
  wrap_db_session.__name__ = f.__name__
  return wrap_db_session

def get_offset_and_limit(f):
  """Normalize offset/limit query string params"""
  def wrap_offset(*args, **kwargs):
    kwargs['query']['offset'] = request.args.get('offset', default=0, type=int)
    kwargs['query']['limit'] = request.args.get('limit', default=DEFAULT_LIMIT, type=int)
    return f(*args, **kwargs)
  wrap_offset.__name__ = f.__name__
  return wrap_offset

def store_uploaded_image(param_name, store=False, uploaded_im_path='static/data/uploaded'):
  """Retrive an uploaded image and prepare for processing. Optionally store it to disk."""
  def decorator(f):
    def wrap_uploaded_image(*args, **kwargs):
      if param_name not in request.files:
        raise APIError('No file uploaded')

      file = request.files[param_name]

      # convert string of image data to uint8
      nparr = np.fromstring(file.read(), np.uint8)

      # decode image
      im = cv.imdecode(nparr, cv.IMREAD_COLOR)

      if store:
        uploaded_im_fn = secure_filename(datetime.now().isoformat() + "_" + file.filename)
        uploaded_im_abspath = os.path.join(uploaded_im_path, uploaded_im_fn)
        uploaded_im_remote_path = os.path.join('/', uploaded_im_path, uploaded_im_fn)
        nparr.tofile(uploaded_im_abspath)
        kwargs['query']['url'] = uploaded_im_remote_path
        kwargs['im'] = im
      return f(*args, **kwargs)
    wrap_uploaded_image.__name__ = f.__name__
    return wrap_uploaded_image
  return decorator

def as_json(f):
  """Output an API query as JSON"""
  def wrap_jsonify(*args, **kwargs):
    return jsonify(f(*args, **kwargs))
  wrap_jsonify.__name__ = f.__name__
  return wrap_jsonify

def exception_handler(f):
  """Handle exceptions caused by the API"""
  def wrapper(*args, **kwargs):
    try:
      return f(*args, **kwargs)
    except Exception as e:
      return {
        "error": True,
        "message": e.message,
        "query": kwargs['query'],
      }
  wrapper.__name__ = f.__name__
  return wrapper

class APIError(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)
