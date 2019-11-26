"""Run a flask server to search an in-memory feature vector store
"""

import click

@click.command('')
@click.option('-i', '--input', 'opt_fp_pickle', required=True)
@click.option('-p', '--port', 'opt_port', default='3000')
@click.pass_context
def cli(ctx, opt_fp_pickle, opt_port):
  """Run a flask server to search an in-memory feature vector store"""

  # ------------------------------------------------
  # imports

  import os
  import pickle
  import logging
  from os.path import join
  from functools import partial
  from glob import glob

  import cv2 as cv

  import numpy as np
  from flask import Flask, request, send_from_directory, jsonify
  
  from app.settings import app_cfg
  from app.models import types
  from app.utils import log_utils, file_utils
  from app.server.decorators import api_query, store_uploaded_image, get_offset_and_limit, as_json, exception_handler

  from app.image import cvdnn
  from app.utils import file_utils

  # ------------------------------------------------
  # load model and vectors

  log = logging.getLogger('vframe')  # move to ctx

  dnn_factory = cvdnn.DNNFactory()  # FIXME: make static class?

  data = file_utils.load_pickle(opt_fp_pickle)
  opt_model_enum = data['model']['enum']
  features = data['features']
  mediaRecords = data['mediaRecords']

  cvmodel = dnn_factory.from_enum(opt_model_enum)

  log.debug(f'Using model: {opt_model_enum} and layer: {cvmodel.dnn_cfg.features}')

  # ------------------------------------------------
  # instantiate flask server

  index_html = 'prod.html' if app_cfg.PRODUCTION else 'dev.html'

  static_folder = os.path.normpath(join(os.getcwd(), '../static'))
  app = Flask('__main__', static_folder=static_folder, static_url_path='/static')

  @app.errorhandler(404)
  def page_not_found(e):
    return app.send_static_file(index_html), 200

  @app.route('/search/', methods=['GET'])
  def index():
    return app.send_static_file(index_html)

  @app.route('/favicon.ico')
  def favicon():
    return send_from_directory(os.path.join(app.root_path, 'img/'),
      'favicon.ico',mimetype='image/vnd.microsoft.icon')

  # ------------------------------------------------
  # api route

  @app.route('/api/v1/search/info', methods=['GET'])
  @as_json
  @exception_handler
  def info(query={}):
    return {
      'features': {
        opt_model_enum.name: cvmodel.dnn_cfg,
      },
      'active': [opt_model_enum.name],
    }

  @app.route('/api/v1/image/upload', methods=['POST'])
  @as_json
  @exception_handler
  @api_query
  @store_uploaded_image('query_img', store=True)
  def upload(im, query={}):
    pass

  @app.route('/api/v1/search/image', methods=['POST'])
  @as_json
  @exception_handler
  @api_query
  @get_offset_and_limit
  @store_uploaded_image('query_img', store=True)
  def search(im, query={}):
    # search_flat_features(im, model, features, mediaRecords)
    query_feat = cvmodel.features(im)
    dists = np.linalg.norm(features - query_feat, axis=1)
    start = query['offset']
    end = query['offset'] + query['limit']
    ids = np.argsort(dists)[start:end] # Sort results
    scores = [{
      'score': dists[id].item(),
      'mediaRecord': mediaRecords[id],
    } for id in ids]

    return scores

  # ------------------------------------------------
  # run the server directly

  app.run("0.0.0.0", port=opt_port)
