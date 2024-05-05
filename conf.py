import os


class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'abcdsacb12312'

    MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'static/uploads')
