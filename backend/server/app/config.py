class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://docker:s3cr3t@postgres:5432/data_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
