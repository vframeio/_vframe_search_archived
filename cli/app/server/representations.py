import simplejson as json
from flask import make_response

def output_json(data, code, headers=None):
  content_type = 'application/json'
  dumped = json.dumps(data)
  if headers:
    headers.update({'Content-Type': content_type})
  else:
    headers = {'Content-Type': content_type}
  response = make_response(dumped, code, headers)
  return response
