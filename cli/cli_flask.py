# --------------------------------------------------------
# wrapper for flask CLI API
# NB: python cli_flask.py run
# --------------------------------------------------------

import click
import sys

from flask.cli import FlaskGroup
from app.server.web import create_app
from app.server.socket import create_socket

cli = FlaskGroup(create_app=create_app)

# --------------------------------------------------------
# Entrypoint
# --------------------------------------------------------
if __name__ == '__main__':
  # circumvent click / werkzeug
  if len(sys.argv) > 1 and sys.argv[1] == 'socket':
    create_socket()
  else:
    cli()
