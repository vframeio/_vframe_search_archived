"""
Enumerated application data types
"""
import os
from os.path import join
from pathlib import Path
from enum import Enum

from app.utils import file_utils, click_utils

SELF_CWD = os.path.dirname(os.path.realpath(__file__))


# ---------------------------------------------------------------------
# Model Zoo
# --------------------------------------------------------------------

def create_modelzoo_enum():
	"""Dynamically create ModelZoo enum type using model zoo YAML
	"""
	DIR_VFRAME_SEARCH = str(Path(SELF_CWD).parent.parent.parent)
	fp_modelzoo = join(DIR_VFRAME_SEARCH, 'modelzoo/modelzoo.yaml')
	#fp_modelzoo = str(Path(SELF_CWD).parent / 'settings/modelzoo.yaml')
	modelzoo_dict = file_utils.load_yaml(fp_modelzoo)
	modelzoo_enums = {}
	for i, kv in enumerate(modelzoo_dict.items()):
	  k,v = kv
	  if v.get('active'):
	    modelzoo_enums.update({k.upper(): i})
	return modelzoo_enums

ModelZoo = Enum('ModelZoo', create_modelzoo_enum())
ModelZooClickVar = click_utils.ParamVar(ModelZoo)


# ---------------------------------------------------------------------
# Media types, items
# --------------------------------------------------------------------

class MediaType(Enum):
  UNKNOWN, TEXT, IMAGE, VIDEO, VIDEO_FRAME = range(5)

MediaTypeName = [
  'unknown', 'text', 'image', 'video', 'video_frame'
]
MediaTypeIndex = { name: i for i, name in enumerate(MediaTypeName) }
MediaTypeClickVar = click_utils.ParamVar(MediaType)


# ---------------------------------------------------------------------
# Logger, monitoring
# --------------------------------------------------------------------
class LogLevel(Enum):
  """Loger vebosity"""
  DEBUG, INFO, WARN, ERROR, CRITICAL = range(5)

LogLevelVar = click_utils.ParamVar(LogLevel)

# ---------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

def find_type(name, enum_type):
  for enum_opt in enum_type:
    if name == enum_opt.name.lower():
      return enum_opt
  return None