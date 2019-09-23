import os
import glob
import time

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

from app.settings import app_cfg

connection_url = "mysql+mysqlconnector://{}:{}@{}/{}?charset=utf8mb4".format(
  os.getenv("DB_USER"),
  os.getenv("DB_PASS"),
  os.getenv("DB_HOST"),
  os.getenv("DB_NAME")
)

engine = create_engine(connection_url, encoding="utf-8", pool_recycle=3600)

Session = sessionmaker(bind=engine)
# Base = declarative_base()

db = SQLAlchemy()

from app.sql.models.media import Media
from app.sql.models.media_feature import MediaFeature
from app.sql.models.media_metadata import MediaMetadata
from app.sql.models.collection import Collection, CollectionForm
from app.sql.models.collection_media import CollectionMedia, CollectionMediaForm
from app.sql.models.upload import Upload
from app.sql.models.feature_type import FeatureType, FeatureTypeForm

for i in range(10):
  try:
    db.Model.metadata.create_all(engine)
    break
  except:
    time.sleep(2)
    if i > 8:
      raise
