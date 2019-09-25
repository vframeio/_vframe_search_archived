from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.datastructures import MultiDict

from app.sql.common import db
# from app.sql.models.collection import Collection, CollectionForm, getMediaCounts
# from app.sql.models.collection_media import CollectionMedia, CollectionMediaForm

class CrudView(FlaskView):
  # to subclass CrudView, specify the model + form:
  # model = Collection
  # form = CollectionForm
  excluded_methods = ['on_index', 'on_show', 'on_create', 'on_update', 'on_destroy']

  # implement these methods:
  def on_index(self, data):
    return data
  def on_show(self, data):
    return data
  def on_create(self, item):
    pass
  def on_update(self, item):
    pass
  def on_destroy(self, item):
    pass

  def index(self):
    """
    List all {model}s
    """
    items = self.model.query.all()
    return jsonify(self.on_index({
      'status': 'ok',
      'res': [ item.toJSON() for item in items ],
    }))

  def get(self, id):
    """
    Fetch a single {model}.
    """
    item = self.model.query.get(id)
    if not item:
      return jsonify({
        'status': 'error',
        'error': 'item not found'
      })
    return jsonify(self.on_show({
      'status': 'ok',
      'res': item.toFullJSON() if hasattr(item, 'toFullJSON') else item.toJSON(),
    }))

  def post(self):
    """
    Create a new {model}.

    * JSON params: {jsonparams}
    """
    raw_form = MultiDict(request.json) if request.json is not None else request.form
    form = self.form(raw_form)
    if form.validate():
      item = self.model()
      form.populate_obj(item)
      self.on_create(item)
      db.session.add(item)
      db.session.commit()
      return jsonify({
        'status': 'ok',
        'res': item.toJSON(),
      })
    return jsonify({
      'error': 'error',
      'errors': form.errors,
    })

  def put(self, id):
    """
    Update a {model}.

    * JSON params: {jsonparams}
    """
    item = self.model.query.get(id)
    if not item:
      return jsonify({
        'status': 'error',
        'error': 'not found',
      })
    raw_form = MultiDict(request.json) if request.json is not None else request.form
    form = self.form(raw_form, obj=item)
    if form.validate():
      form.populate_obj(item)
      self.on_update(item)
      db.session.add(item)
      db.session.commit()
      return jsonify({
        'status': 'ok',
        'res': item.toJSON(),
      })

  def delete(self, id):
    """
    Delete a {model}.
    """
    item = self.model.query.get(id)
    if not item:
      return jsonify({
        'status': 'error',
        'error': 'not found',
      })

    self.on_destroy(item)
    db.session.delete(item)
    db.session.commit()
    return jsonify({
      'status': 'ok',
    })
