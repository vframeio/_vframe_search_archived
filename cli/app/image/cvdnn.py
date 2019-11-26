from os.path import join
import logging
from pathlib import Path

import cv2 as cv
import numpy as np
import dacite

from app.models.rect import RectNorm, RectDim
from app.models.cvmodels import NetConfig
from app.models.cvmodels import ClassifyResult, ClassifyResults
from app.models.cvmodels import DetectResult, DetectResults
from app.utils import file_utils
from app.settings import app_cfg

log = logging.getLogger('vframe')


class OpenCVDNN:
  
  def __init__(self, dnn_cfg):
    self.log = logging.getLogger('vframe')
    self.dnn_cfg = dnn_cfg
    # set filepaths
    fp_model = join(app_cfg.DIR_MODELS, dnn_cfg.model)
    fp_config = join(app_cfg.DIR_MODELS, dnn_cfg.config)
    fp_labels = join(app_cfg.DIR_MODELS, dnn_cfg.labels)
    # build dnn net
    self.log.debug(f'Create DNN net using: {dnn_cfg.framework}')
    if dnn_cfg.framework == 'onnx':
      self.net = cv.dnn.readNetFromONNX(fp_model)
    else:
      self.net = cv.dnn.readNet(fp_model, fp_config, dnn_cfg.framework)
    self.net.setPreferableBackend(dnn_cfg.dnn_backend)
    self.net.setPreferableTarget(dnn_cfg.dnn_target)
    if Path(fp_labels).is_file():
      self.labels = file_utils.load_text(fp_labels)  # line-delimited list of class labels
    else:
      self.log.warn(f'labels file does not exist: {fp_labels}')
      self.labels = []
    
  def _preprocess(self, im):
    c = self.dnn_cfg
    im = cv.resize(im, c.size, cv.INTER_CUBIC)
    self.frame_dim = im.shape[:2][::-1]
    blob = cv.dnn.blobFromImage(im, c.scale , c.size, c.mean, crop=c.crop, swapRB=c.rgb)
    self.net.setInput(blob)
    
  def features(self, im):
    cfg = self.dnn_cfg
    self._preprocess(im)
    feat_vec = np.squeeze(self.net.forward(cfg.features).flatten())
    return feat_vec / np.linalg.norm(feat_vec)
  
  def perf_ms(self):
    """Returns network forward pass performance time in milliseconds"""
    t, _ = self.net.getPerfProfile()
    return t * 1000.0 / cv.getTickFrequency()


class Classifier(OpenCVDNN):
    
  def infer(self, im, limit=1, threshold=None):
    threshold = threshold if threshold is not None else self.dnn_cfg.threshold
    self._preprocess(im)
    preds = self.net.forward().flatten()
    if limit > 1:
      idxs = np.argsort(preds)[::-1][:limit]  # top N indices
    else:
      idxs = [np.argmax(preds)]
    results = [ClassifyResult(i, preds[i], self.labels[i]) for i in idxs if preds[i] > threshold]
    dnn_results = ClassifyResults(results, self.perf_ms())
    return dnn_results


class Detector(OpenCVDNN):
  
  nms_threshold = 0.4  # non-maximum suppression

  def infer(self, im, threshold=0.8, limit=10):
    threshold = threshold if threshold is not None else self.dnn_cfg.threshold
    self._preprocess(im)
    if self.dnn_cfg.framework == 'darknet':
      out_names = self.net.getUnconnectedOutLayersNames()
      outs = self.net.forward(out_names)
    else:
      outs = self.net.forward()

    # OpenCV
    class_idxs = []
    confidences = []
    boxes = []
    detect_results = []

    layer_names = self.net.getLayerNames()
    last_layer_names = self.net.getLayerId(layer_names[-1])
    last_layer = self.net.getLayer(last_layer_names)

    if last_layer.type == 'DetectionOutput':
      # Network produces output blob with a shape 1x1xNx7 where N is a number of
      # outs and an every detection is a vector of values
      # [batchId, class_idx, confidence, left, top, right, bottom]
      #for detection in outs[0,0,:,:]:
      for detection in outs[0, 0]:
        confidence = float(detection[2])
        if confidence > threshold:
          class_idx = int(detection[1])  # skip background ?
          (x1,y1,x2,y2) = detection[3:7]
          rect_norm = RectNorm(x1,y1,x2,y2)
          rect_dim_xywh = rect_norm.to_rect_dim(self.frame_dim).as_xywh()
          try:
            label = self.labels[class_idx] if self.labels else ''
          except Exception as e:
            self.log.error(f'Class index: {class_idx} out of bounds in {len(self.labels)} list')
          # for nms
          confidences.append(float(confidence))
          boxes.append(rect_dim_xywh)
          # for return
          detect_result = DetectResult(class_idx, confidence, rect_norm, label)
          detect_results.append(detect_result)

    elif last_layer.type == 'Region':
      # Network produces output blob with a shape NxC where N is a number of
      # detected objects and C is a number of classes + 4 where the first 4
      # numbers are [center_x, center_y, width, height]
      for out in outs:
        for detection in out:
          scores = detection[5:]
          class_idx = np.argmax(scores)
          confidence = scores[class_idx]
          if confidence > self.dnn_cfg.threshold:
            cx, cy, w, h = detection[0:4]
            rect_norm = RectNorm.from_cxcywh(cx, cy, w, h)
            rect_dim = rect_norm.to_rect_dim(self.frame_dim)
            rect_dim_xywh = rect_norm.to_rect_dim(self.frame_dim).as_xywh()
            label = self.labels[class_idx] if self.labels else ''
            # for nms
            confidences.append(float(confidence))
            boxes.append(rect_dim_xywh)
            # for return
            detect_result = DetectResult(class_idx, confidence, rect_norm, label)
            detect_results.append(detect_result)
    else:
      self.log.error(f'Unknown output layer type: {last_layer.type}')
      return

    if self.dnn_cfg.nms:
      # apply non-maximum suppression and filter detection results
      idxs = cv.dnn.NMSBoxes(boxes, confidences, self.dnn_cfg.threshold, self.nms_threshold)
      detect_results = [detect_results[i[0]] for i in idxs]
      
    dnn_result = DetectResults(detect_results, self.perf_ms())
    return dnn_result

# ---------------------------------------------------------------------------
# DNN CV Model factory
# ---------------------------------------------------------------------------

class DNNFactory:

  net_config_types = {
    'classification': Classifier,
    'object_detection': Detector
  }

  def __init__(self):
    self.log = logging.getLogger('vframe')


  def from_cfg(self, cfg):
    '''Creates DNN model based on configuration from modelzoo
    :param name: name of model in the modelzoo configuration YAML
    :returns (OpenCVDNN):
    '''
    dnn_cfg = dacite.from_dict(data_class=NetConfig, data=cfg)
    return self.from_dnn_cfg(dnn_cfg)


  def from_dnn_cfg(self, dnn_cfg):
    '''Creates DNN model based on configuration from modelzoo
    :param name: name of model in the modelzoo configuration YAML
    :returns (OpenCVDNN):
    '''
    dnn_net = self.net_config_types.get(dnn_cfg.task_type)
    return dnn_net(dnn_cfg)


  def from_enum(self, enum_obj):
    '''Creates DNN model based on configuration from modelzoo
    :param name: name of model in the modelzoo configuration YAML
    :returns (OpenCVDNN):
    '''
    name = enum_obj.name.lower()
    cfg = app_cfg.MODELZOO_CFG.get(name)
    return self.from_cfg(cfg)