import os

dir_base = os.path.abspath(os.path.join(os.path.dirname(__file__)))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dir_base, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
