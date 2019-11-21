#!/usr/bin/env python

import click

from app.settings import app_cfg
from app.utils import log_utils
from app.controllers.click_factory import ClickSimple


if __name__ == '__main__':

  import sys
  import argparse

  # argparse: intercept group
  argv_tmp = sys.argv
  sys.argv = sys.argv[:2]
  ap = argparse.ArgumentParser('\033[1m\033[94mVFRAME\033[0m')
  ap.add_argument('group', choices=app_cfg.CLICK_GROUPS.keys())
  args = ap.parse_args()
  sys.argv = argv_tmp
  sys.argv.pop(1)  # remove group

  # special cases: Flask, DB
  if args.group == 'flask':
    
    from flask.cli import FlaskGroup
    from app.server.web import create_app
    from app.server.socket import create_socket

    if len(sys.argv) > 1 and sys.argv[1] == 'socket':
      cli = create_socket
    else:
      cli = FlaskGroup(create_app=create_app)

  elif args.group == 'db':

    import re
    from alembic.config import main

    if __name__ == '__main__':
      sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
      sys.exit(main())

  else:

    # click: parse rest of argv
    cc = ClickSimple.create(app_cfg.CLICK_GROUPS[args.group])
    @click.group(cls=cc, chain=False, no_args_is_help=True)
    @click.option('-v', '--verbose', 'opt_verbosity', count=True, default=4, 
      show_default=True,
      help='Verbosity: -v DEBUG, -vv INFO, -vvv WARN, -vvvv ERROR, -vvvvv CRITICAL')
    @click.option('--log', 'opt_fp_log', help='Path to logfile')
    @click.pass_context
    def cli(ctx, opt_verbosity, opt_fp_log):
      """\033[1m\033[94mVFRAME: Search\033[0m                                                
      """
      ctx.opts = {}
      log_utils.Logger.create(verbosity=opt_verbosity, logfile=opt_fp_log)

  # entrypoint
  cli()