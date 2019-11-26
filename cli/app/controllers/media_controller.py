from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict
from sqlalchemy.sql.expression import func
from random import randrange
import os

from app.settings import app_cfg
from app.sql.common import db
from app.sql.models.media import Media
from app.sql.models.upload import Upload

class MediaView(FlaskView):
  def index(self):
    """
    List all media.

    * Query string params: offset, limit, sort (id, date), order (asc, desc)
    """
    medias = Media.query.limit(50)
    print(medias[0])
    return jsonify({
      'status': 'ok',
      'res': [ media.toJSON() for media in medias ],
    })

  def info(self):
    """
    Get info about the quantity of media in the database, including free disk space.
    """
    count_query = (Media.query.statement.with_only_columns([func.count()]).order_by(None))
    mediaCount = db.session.execute(count_query).scalar()
    count_query = (Upload.query.statement.with_only_columns([func.count()]).order_by(None))
    uploadCount = db.session.execute(count_query).scalar()
    st = os.statvfs(app_cfg.DIR_DATA_STORE)
    freeSpace = st.f_bavail * st.f_frsize / 1024 / 1024 / 1024
    return jsonify({
      'status': 'ok',
      'res': {
        'mediaCount': mediaCount,
        'uploadCount': uploadCount,
        'freeSpace': freeSpace,
      }
    })

  def id(self, id):
    """
    Fetch a single media by ID.
    """
    media = Media.query.get(id)
    return jsonify({
      'status': 'ok',
      'res': media.toFullJSON(),
    })

  def sha256(self, hash: str):
    """
    Fetch a single media by SHA256.
    """
    if len(hash) != 64:
      return jsonify({
        'status': 'error',
        'error': 'bad hash',
      })
    media = Media.query.filter_by(sha256=hash).first()
    return jsonify({
      'status': 'ok',
      'res': media.toFullJSON(),
    })

  def random(self):
    """
    Fetch a random media.
    """
    count = db.session.query(Media).count()
    if count == 0:
      return jsonify({ 'status': 'error', 'error': 'Database empty' })
    while True:
      rand = randrange(0, count)
      row = db.session.query(Media)[rand]
      if row.mediaType == 'image' or row.mediaType == 'video_frame':
        break
    return jsonify({
      'status': 'ok',
      'res': row.toFullJSON(),
    })
