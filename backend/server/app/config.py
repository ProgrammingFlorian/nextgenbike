import os

import os
from pathlib import Path

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = "postgresql://docker:s3cr3t@localhost:12345/data_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
