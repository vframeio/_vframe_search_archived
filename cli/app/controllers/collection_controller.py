from flask import request, jsonify, redirect
from flask_classful import route
from werkzeug.datastructures import MultiDict

from app.sql.common import db
from app.sql.models.collection import Collection, CollectionForm, getMediaCounts
from app.sql.models.collection_media import CollectionMedia, CollectionMediaForm
from app.controllers.crud_controller import CrudView

from app.data.export import export_zip

class CollectionView(CrudView):
  model = Collection
  form = CollectionForm
  route_prefix = '/collection/'

  def on_index(self, data):
    data['counts'] = getMediaCounts()
    return data

  def on_destroy(self, item):
    db.session.query(CollectionMedia).filter(CollectionMedia.collection_id == item.id).delete(synchronize_session=False)

  @route('/<id>/media/', methods=['POST'])
  def add_collection_media(self, id: int):
    """
    Add media to a collection.

    * JSON params: media_id, username
    """
    collection = Collection.query.get(id)
    if not collection:
      return jsonify({
        'status': 'error',
        'error': 'not found',
      })
    raw_form = MultiDict(request.json) if request.json is not None else request.form
    form = CollectionMediaForm(raw_form)
    if form.validate():
      collection_media = CollectionMedia()
      form.populate_obj(collection_media)
      db.session.add(collection_media)
      db.session.commit()
      return jsonify({
        'status': 'ok',
        'res': collection_media.toJSON(),
      })
    return jsonify({
      'status': 'error',
      'error': 'validation error',
    })

  @route('/<id>/media/<media_id>/', methods=['DELETE'])
  def destroy_collection_media(self, id: int, media_id: int):
    """
    Remove media from a collection.
    """
    collection_media = CollectionMedia.query.get((id, media_id,))
    if collection_media:
      db.session.delete(collection_media)
      db.session.commit()
      return jsonify({
        'status': 'ok',
      })
    return jsonify({
      'status': 'error',
      'error': 'not found',
    })

  @route('/<id>/export/', methods=['GET'])
  def export_collection(self, id: int):
    """
    Export a collection as a ZIP file
    """
    zip_url = export_zip(id)
    if request.args.get('redirect') == '1':
      print(zip_url)
      return redirect(zip_url, code=302)
    return jsonify({
      'status': 'success',
      'url': zip_url,
    })
