
from pymediainfo import MediaInfo

def mediainfo(fp_in):
  """Returns abbreviated video/audio metadata for video files
  :param fp_in: filepath"""
  
  result = {}
  media_info_raw = MediaInfo.parse(fp_in).to_data()

  for d in media_info_raw['tracks']:
    if d['track_type'] == 'Video':
      result = {
        'codec_cc': d['codec_cc'],
        'duration': int(d['duration']),
        'display_aspect_ratio': float(d['display_aspect_ratio']),
        'width': int(d['width']),
        'height': int(d['height']),
        'frame_rate': float(d['frame_rate']),
        'frame_count': int(d['frame_count']),
        }
  
  return result