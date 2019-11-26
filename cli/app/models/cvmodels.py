from os.path import join
from dataclasses import dataclass

import cv2 as cv

from app.models.rect import RectNorm, RectDim


@dataclass
class NetConfig:
  name: str
  framework: str
  task_type: str
  model: str
  config: str
  threshold: float
  mean: list
  scale: float
  width: int
  height: int
  rgb: bool
  crop: bool
  dimensions: int = 0
  labels: str = ''
  features: str = ''
  nms: bool = False
  
  @property
  def size(self):
    return (self.width, self.height)
  
  @property
  def dnn_backend(self):
    props = {
      'DEFAULT': cv.dnn.DNN_BACKEND_DEFAULT,
      'HALIDE': cv.dnn.DNN_BACKEND_HALIDE,
      'INFERENCE_ENGINE': cv.dnn.DNN_BACKEND_INFERENCE_ENGINE,
      'OPENCV': cv.dnn.DNN_BACKEND_OPENCV,
      'VKCOM': cv.dnn.DNN_BACKEND_VKCOM
    }
    try:
      # throws exception if backend was not yet (overrides default value issue)
      prop = props.get(self.backend)
    except Exception as e:
      prop = props.get('DEFAULT')
    return prop
    
  @property
  def dnn_target(self):
    props = {
      'CPU': cv.dnn.DNN_TARGET_CPU,
      'FPGA': cv.dnn.DNN_TARGET_FPGA,
      'MYRIAD': cv.dnn.DNN_TARGET_MYRIAD,
      'OPENCL': cv.dnn.DNN_TARGET_OPENCL,
      'OPENCL_FP16': cv.dnn.DNN_TARGET_OPENCL_FP16,
      'VULKAN': cv.dnn.DNN_TARGET_VULKAN
    }
    try:
      # throws exception if backend was not yet (overrides default value issue)
      prop = props.get(self.backend)
    except Exception as e:
      prop = props.get('CPU')
    return prop

  

# ---------------------------------------------------------
# Prediction results

@dataclass
class PredictResult:
  index: int
  confidence: float
  def toJSON(self):
    return {
      'index': self.index,
      'confidence': float(self.confidence),
    }

    
# ---------------------------------------------------------
# Classify result

@dataclass
class ClassifyResult(PredictResult):
  label: str
  def toJSON(self):
    return {
      'label': self.label,
    }

@dataclass
class ClassifyResults:
  classifications: list
  duration: float
  task_type: str = 'classification'
  def toJSON(self):
    return {
      'classifications': [ d.toJSON() for d in self.classifications ],
      'duration': float(self.duration),
      'task_type': self.task_type,
    }

@dataclass
class DetectResult(PredictResult):
  rect: RectNorm
  label: str = ''
  def toJSON(self):
    return {
      'rect': self.rect.toJSON(),
      'label': self.label,
    }

@dataclass
class DetectResults:
  detections: list
  duration: float
  task_type: str = 'detection'
  def toJSON(self):
    return {
      'detections': [ d.toJSON() for d in self.detections ],
      'duration': float(self.duration),
      'task_type': self.task_type,
    }
