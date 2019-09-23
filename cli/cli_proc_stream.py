# --------------------------------------------------------
# add/edit commands in commands/datasets directory
# --------------------------------------------------------

from functools import update_wrapper, wraps

import click

from app.settings import app_cfg as cfg
from app.utils import log_utils
from app.utils.click_factory import ClickComplex

# click cli factory
cc = ClickComplex.create(cfg.DIR_COMMANDS_PROCESS)
 
# --------------------------------------------------------
# CLI
# --------------------------------------------------------
@click.group(cls=cc, chain=False)
@click.option('-v', '--verbose', 'verbosity', count=True, default=4, 
  show_default=True,
  help='Verbosity: -v DEBUG, -vv INFO, -vvv WARN, -vvvv ERROR, -vvvvv CRITICAL')
@click.pass_context
def cli(ctx, **kwargs):
  """\033[1m\033[94mVFRAME:Image Processing Modules\033[0m                                                
  """
  ctx.opts = {}
  # init logger
  log_utils.Logger.create(verbosity=kwargs['verbosity'])


@cli.resultcallback()
def process_commands(processors, **kwargs):
  """This result callback is invoked with an iterable of all the chained
  subcommands.  As in this example each subcommand returns a function
  we can chain them together to feed one into the other, similar to how
  a pipe on unix works.

  This function was copied from click's documentation.
  """

  def sink():
    """This is the end of the pipeline"""
    while True:
      yield

  sink = sink()
  sink.__next__()
  # sink.next()
  #try:
  #  sink.__next__()
  #except Exception as ex:
  #  logging.getLogger('vframe').error('{} (can\'t view here)'.format(ex))
  #  return

  # Compose all of the coroutines, and prime each one
  for processor in reversed(processors):
    sink = processor(sink)
    sink.__next__()
    # sink.next()
    # try:
    #   sink.__next__()
    # except Exception as ex:
    #   logging.getLogger('vframe').error('error: {} (can\'t view here)'.format(ex))
    #   return

  sink.close() # this executes the whole pipeline.
               # however it is unnecessary, as close() would be automatically
               # called when sink goes out of scope here.
                 
def processor(f):
  """Helper decorator to rewrite a function so that it returns another
  function from it.

  This function was copied from click's documentation.
  """
  def processor_wrapper(*args, **kwargs):
      @wraps(f)
      def processor(sink):
          return f(sink, *args, **kwargs)
      return processor
  return update_wrapper(processor_wrapper, f)


def generator(f):
  """Similar to the :func:`processor` but passes through old values
  unchanged.
  """
  @processor
  def _generator(sink, *args, **kwargs):
      try:
          while True:
              sink.send((yield))
      except GeneratorExit:
          f(sink, *args, **kwargs)
          sink.close()
  return update_wrapper(_generator, f)

# --------------------------------------------------------
# Entrypoint
# --------------------------------------------------------
if __name__ == '__main__':
    cli()
