import sys
from math import sqrt
import logging

import numpy as np
import cv2 as cv

log = logging.getLogger('vframe')


# ---------------------------------------------------------------------------
# 3D landmark drawing utilities
# ---------------------------------------------------------------------------

end_list = np.array([17, 22, 27, 42, 48, 31, 36, 68], dtype=np.int32) - 1

def plot_keypoints(im, kpts):
  '''Draw 68 key points
  :param im: the input im
  :param kpts: (68, 3). flattened list
  '''
  im = im.copy()
  kpts = np.round(kpts).astype(np.int32)
  for i in range(kpts.shape[0]):
    st = kpts[i, :2]
    im = cv.circle(im, (st[0], st[1]), 1, (0, 0, 255), 2)
    if i in end_list:
      continue
    ed = kpts[i + 1, :2]
    im = cv.line(im, (st[0], st[1]), (ed[0], ed[1]), (255, 255, 255), 1)
  return im


def calc_hypotenuse(pts):
  bbox = [min(pts[0, :]), min(pts[1, :]), max(pts[0, :]), max(pts[1, :])]
  center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
  radius = max(bbox[2] - bbox[0], bbox[3] - bbox[1]) / 2
  bbox = [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius]
  llength = sqrt((bbox[2] - bbox[0]) ** 2 + (bbox[3] - bbox[1]) ** 2)
  return llength / 3

def build_camera_box(rear_size=90):
  point_3d = []
  rear_depth = 0
  point_3d.append((-rear_size, -rear_size, rear_depth))
  point_3d.append((-rear_size, rear_size, rear_depth))
  point_3d.append((rear_size, rear_size, rear_depth))
  point_3d.append((rear_size, -rear_size, rear_depth))
  point_3d.append((-rear_size, -rear_size, rear_depth))

  front_size = int(4 / 3 * rear_size)
  front_depth = int(4 / 3 * rear_size)
  point_3d.append((-front_size, -front_size, front_depth))
  point_3d.append((-front_size, front_size, front_depth))
  point_3d.append((front_size, front_size, front_depth))
  point_3d.append((front_size, -front_size, front_depth))
  point_3d.append((-front_size, -front_size, front_depth))
  point_3d = np.array(point_3d, dtype=np.float).reshape(-1, 3)

  return point_3d


def plot_pose_box(im, Ps, pts68s, color=(40, 255, 0), line_width=2):
  '''Draw a 3D box as annotation of pose. 
    ref: https://github.com/yinguobing/head-pose-estimation/blob/master/pose_estimator.py
  :param image: the input image
  :param P: (3, 4). Affine Camera Matrix.
  :param kpts: (2, 68) or (3, 68)
  '''
  im_draw = im.copy()
  if not isinstance(pts68s, list):
    pts68s = [pts68s]
  
  if not isinstance(Ps, list):
    Ps = [Ps]
  
  for i in range(len(pts68s)):
    pts68 = pts68s[i]
    llength = calc_hypotenuse(pts68)
    point_3d = build_camera_box(llength)
    P = Ps[i]

    # Map to 2d im points
    point_3d_homo = np.hstack((point_3d, np.ones([point_3d.shape[0], 1])))  # n x 4
    point_2d = point_3d_homo.dot(P.T)[:, :2]

    point_2d[:, 1] = - point_2d[:, 1]
    point_2d[:, :2] = point_2d[:, :2] - np.mean(point_2d[:4, :2], 0) + np.mean(pts68[:2, :27], 1)
    point_2d = np.int32(point_2d.reshape(-1, 2))

    # Draw all the lines
    cv.polylines(im_draw, [point_2d], True, color, line_width, cv.LINE_AA)
    cv.line(im_draw, tuple(point_2d[1]), tuple(point_2d[6]), color, line_width, cv.LINE_AA)
    cv.line(im_draw, tuple(point_2d[2]), tuple(point_2d[7]), color, line_width, cv.LINE_AA)
    cv.line(im_draw, tuple(point_2d[3]), tuple(point_2d[8]), color, line_width, cv.LINE_AA)

    return im_draw



# ---------------------------------------------------------------------------
#
# OpenCV drawing functions
#
# ---------------------------------------------------------------------------

pose_types = {'pitch': (0,0,255), 'roll': (255,0,0), 'yaw': (0,255,0)}

def draw_landmarks2D(im, points_norm, radius=3, color=(0,255,0)):
  '''Draws facial landmarks, either 5pt or 68pt
  '''
  im_dst = im.copy()
  dim = im.shape[:2][::-1]
  for x,y in points_norm:
    pt = (int(x*dim[0]), int(y*dim[1]))
    cv.circle(im_dst, pt, radius, color, -1, cv.LINE_AA)
  return im_dst

def draw_landmarks3D(im, points, radius=3, color=(0,255,0)):
  '''Draws 3D facial landmarks
  '''
  im_dst = im.copy()
  for x,y,z in points:
    cv.circle(im_dst, (x,y), radius, color, -1, cv.LINE_AA)
  return im_dst

def draw_bbox(im, bbox_norm, color=(0,255,0), stroke_weight=2):
  '''Draws BBox onto cv image
  '''
  im_dst = im.copy()
  bbox_dim = bbox_norm.to_bbox_dim(im.shape[:2][::-1])
  cv.rectangle(im_dst, bbox_dim.p1.xy, bbox_dim.p2.xy, color, stroke_weight, cv.LINE_AA)
  return im_dst

def draw_pose(im, pt_nose, image_pts):
  '''Draws 3-axis pose over image
  TODO: normalize point data
  '''
  im_dst = im.copy()
  log.debug(f'pt_nose: {pt_nose}')
  log.debug(f'image_pts pitch: {image_pts["pitch"]}')
  cv.line(im_dst, pt_nose, tuple(image_pts['pitch']), pose_types['pitch'], 3)
  cv.line(im_dst, pt_nose, tuple(image_pts['yaw']), pose_types['yaw'], 3)
  cv.line(im_dst, pt_nose, tuple(image_pts['roll']), pose_types['roll'], 3)
  return im_dst

def draw_text(im, pt_norm, text, size=1.0, color=(0,255,0)):
  '''Draws degrees as text over image
  '''
  im_dst = im.copy()
  dim = im.shape[:2][::-1]
  pt = tuple(map(int, (pt_norm[0]*dim[0], pt_norm[1]*dim[1])))
  cv.putText(im_dst, text, pt, cv.FONT_HERSHEY_SIMPLEX, size, color, thickness=1, lineType=cv.LINE_AA)
  return im_dst

def draw_degrees(im, pose_data, color=(0,255,0)):
  '''Draws degrees as text over image
  '''
  im_dst = im.copy()
  for i, pose_type in enumerate(pose_types.items()):
    k, clr = pose_type
    v = pose_data[k]
    t = '{}: {:.2f}'.format(k, v)
    origin = (10, 30 + (25 * i))
    cv.putText(im_dst, t, origin, cv.FONT_HERSHEY_SIMPLEX, 0.5, clr, thickness=2, lineType=2)
  return im_dst