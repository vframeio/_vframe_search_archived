from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
import os
import numpy as np
import cv2 as cv

from app.settings import app_cfg
from app.sql.common import db
from app.sql.models.upload import Upload
from app.utils.file_utils import sha256_stream, sha256_tree, VALID_IMAGE_EXTS
from app.server.decorators import APIError

class UploadView(FlaskView):
  def index(self):
    """
    List all uploaded files.

    * Query string params: offset, limit, sort (id, date), order (asc, desc)
    """
    uploads = Upload.query.all()
    return jsonify({
      'status': 'ok',
      'res': [ upload.toJSON() for upload in uploads ],
    })

  def get(self, id):
    """
    Fetch a single upload.
    """
    upload = Upload.query.get(id)
    return jsonify({
      'status': 'ok',
      'res': upload.toJSON(),
    })

  def post(self):
    """
    Upload a new file.

    * JSON params: username
    """

    try:
      username = request.form.get('username')
    except:
      raise APIError('No username specified')

    param_name = 'image'
    if param_name not in request.files:
      raise APIError('No file uploaded')

    file = request.files[param_name]

    # get sha256
    sha256 = sha256_stream(file)
    _, ext = os.path.splitext(file.filename)
    if ext == '.jpeg':
      ext = '.jpg'

    # TODO: here check sha256
    # upload = Upload.query.get(id)

    if ext[1:] not in VALID_IMAGE_EXTS:
      return jsonify({ 'status': 'error', 'error': 'Not a valid image' })

    # convert string of image data to uint8
    file.seek(0)
    nparr = np.fromstring(file.read(), np.uint8)

    # decode image
    try:
      im = cv.imdecode(nparr, cv.IMREAD_COLOR)
    except:
      return jsonify({ 'status': 'error', 'error': 'Image parse error' })

    upload = Upload.query.filter_by(sha256=sha256).first()
    if upload is not None:
      print("Already uploaded image")
      return jsonify({
        'status': 'ok',
        'notes': 'Image already uploaded',
        'res': upload.toJSON(),
      })

    uploaded_im_fn = secure_filename(sha256 + ext)
    uploaded_im_abspath = os.path.join(app_cfg.DIR_UPLOADS, sha256_tree(sha256))
    uploaded_im_fullpath = os.path.join(uploaded_im_abspath, uploaded_im_fn)

    os.makedirs(uploaded_im_abspath, exist_ok=True)
    nparr.tofile(uploaded_im_fullpath)

    upload = Upload(username=username, sha256=sha256, ext=ext)
    db.session.add(upload)
    db.session.commit()
    return jsonify({
      'status': 'ok',
      'res': upload.toJSON(),
    })

  def delete(self, id):
    """
    Delete an uploaded file.
    """
    upload = Upload.query.get(id)
    if not upload:
      return jsonify({
        'status': 'error',
        'error': 'not found',
      })

    sha256 = upload.sha256

    uploaded_im_fn = secure_filename(sha256 + upload.ext)
    uploaded_im_abspath = os.path.join(app_cfg.DIR_UPLOADS, sha256_tree(sha256))
    uploaded_im_fullpath = os.path.join(uploaded_im_abspath, uploaded_im_fn)
    if os.path.exists(uploaded_im_fullpath):
      print("Removing " + uploaded_im_fullpath)
      os.remove(uploaded_im_fullpath)

    db.session.delete(upload)
    db.session.commit()
    return jsonify({
      'status': 'ok',
      'id': id,
    })
