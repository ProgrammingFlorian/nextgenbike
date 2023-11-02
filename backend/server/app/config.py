import os

import os
from pathlib import Path

dir_base = os.path.abspath(os.path.join(os.path.dirname(__file__)))
dir_parent = os.path.join(dir_base, os.pardir)
dir_database = os.path.join(dir_parent, 'etc/data_db/')

Path(dir_database).mkdir(parents=True, exist_ok=True)

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(dir_database, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
