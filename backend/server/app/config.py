import os

import os

dir_base = os.path.abspath(os.path.join(os.path.dirname(__file__)))
dir_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
dir_database = os.path.join(dir_parent, 'etc/data_db/app.db')

print(dir_database)

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + dir_database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
