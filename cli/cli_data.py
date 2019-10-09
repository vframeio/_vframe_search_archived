# --------------------------------------------------------
# Simple image search over a directory of images.
# --------------------------------------------------------

import click

from app.settings import click_cfg
from app.utils import log_utils
from app.utils.click_factory import ClickSimple

# click cli factory
cc = ClickSimple.create(click_cfg.DIR_COMMANDS_DATA)

# --------------------------------------------------------
# CLI
# --------------------------------------------------------
@click.group(cls=cc, chain=False)
@click.option('-v', '--verbose', 'verbosity', count=True, default=4,
  show_default=True,
  help='Verbosity: -v DEBUG, -vv INFO, -vvv WARN, -vvvv ERROR, -vvvvv CRITICAL')
@click.pass_context
def cli(ctx, **kwargs):
  """\033[1m\033[94mVFRAME: Simple Image Search\033[0m
  """
  ctx.opts = {}
  log_utils.Logger.create(verbosity=kwargs['verbosity'])


# --------------------------------------------------------
# Entrypoint
# --------------------------------------------------------
if __name__ == '__main__':
  cli()

