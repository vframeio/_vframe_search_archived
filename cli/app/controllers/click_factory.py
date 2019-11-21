"""
Click processor factory
- Inspired by and used code from @wiretapped's HTSLAM codebase
- In particular the very useful 
"""

import os
import sys
from os.path import join
from pathlib import Path
import os
from os.path import join
import sys
from functools import update_wrapper, wraps
import itertools
from pathlib import Path
from glob import glob
import importlib
import logging

import click
from app.settings import app_cfg as cfg


# --------------------------------------------------------
# Click Group Class
# --------------------------------------------------------

# set global variable during parent class create
dir_plugins = None  # set in create

class ClickComplex:
  """Wrapper generator for custom Click CLI's based on LR's coroutine"""

  def __init__(self):
    pass


  class CustomGroup(click.Group):
    #global dir_plugins  # from CliGenerator init

    # lists commands in plugin directory
    def list_commands(self, ctx):
      global dir_plugins  # from CliGenerator init
      rv = list(self.commands.keys())
      fp_cmds = [Path(x) for x in Path(dir_plugins).iterdir() \
        if str(x).endswith('.py') \
        and '__init__' not in str(x)]
      for fp_cmd in fp_cmds:
        try:
          assert fp_cmd.name not in rv, "[-] Error: {} can't exist in cli.py and {}".format(fp_cmd.name)
        except Exception as ex:
          logging.getLogger('app').error('{}'.format(ex))
        rv.append(fp_cmd.stem)
      rv.sort()
      return rv

    # Complex version: gets commands in directory and in this file
    # Based on code from @wiretapped + HTSLAM
    def get_command(self, ctx, cmd_name):
      global dir_plugins 
      if cmd_name in self.commands:
       return self.commands[cmd_name]
      ns = {}
      fpp_cmd = Path(dir_plugins, cmd_name + '.py')
      fp_cmd = fpp_cmd.as_posix()
      if not fpp_cmd.exists():
        sys.exit('[-] {} file does not exist'.format(fpp_cmd))
      code = compile(fpp_cmd.read_bytes(), fp_cmd, 'exec')
      try:
        eval(code, ns, ns)
      except Exception as ex:
        logging.getLogger('vframe').error('exception: {}'.format(ex))
        @click.command()
        def _fail():
          raise Exception('while loading {}'.format(fpp_cmd.name))
        _fail.short_help = repr(ex)
        _fail.help = repr(ex)
        return _fail
      if 'cli' not in ns:
        sys.exit('[-] Error: {} does not contain a cli function'.format(fp_cmd))
      return ns['cli']

  @classmethod
  def create(self, dir_plugins_local):
    global dir_plugins
    dir_plugins = dir_plugins_local
    return self.CustomGroup



class ClickSimple:
  """Wrapper generator for custom Click CLI's"""

  def __init__(self):
    pass


  class CustomGroup(click.Group):
    #global dir_plugins  # from CliGenerator init

    # lists commands in plugin directory
    def list_commands(self, ctx):
      global dir_plugins  # from CliGenerator init
      rv = list(self.commands.keys())
      fp_cmds = [Path(x) for x in Path(dir_plugins).iterdir() \
        if str(x).endswith('.py') \
        and '__init__' not in str(x)]
      for fp_cmd in fp_cmds:
        assert fp_cmd.name not in rv, "[-] Error: {} can't exist in cli.py and {}".format(fp_cmd.name)
        rv.append(fp_cmd.stem)
      rv.sort()
      return rv

    # Complex version: gets commands in directory and in this file
    # from HTSLAM
    def get_command(self, ctx, cmd_name):
      global dir_plugins  # from CliGenerator init
      if cmd_name in self.commands:
       return self.commands[cmd_name]
      ns = {}
      fpp_cmd = Path(dir_plugins, cmd_name + '.py')
      fp_cmd = fpp_cmd.as_posix()
      if not fpp_cmd.exists():
        sys.exit('[-] {} file does not exist'.format(fpp_cmd))
      code = compile(fpp_cmd.read_bytes(), fp_cmd, 'exec')
      try:
        eval(code, ns, ns)
      except Exception as ex:
        logging.getLogger('vframe').error('exception: {}'.format(ex))
        @click.command()
        def _fail():
          raise Exception('while loading {}'.format(fpp_cmd.name))
        _fail.short_help = repr(ex)
        _fail.help = repr(ex)
        return _fail
      if 'cli' not in ns:
        sys.exit('[-] Error: {} does not contain a cli function'.format(fp_cmd))
      return ns['cli']

  @classmethod
  def create(self, dir_plugins_local):
    global dir_plugins
    dir_plugins = dir_plugins_local
    return self.CustomGroup
