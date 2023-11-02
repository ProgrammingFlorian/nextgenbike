import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, '/etc/app/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
