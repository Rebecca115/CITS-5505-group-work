import os

class Config(object):
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Secret key for signing cookies
    SECRET_KEY = 'abcdsacb12312'

    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    DEBUG = os.environ.get('FLASK_DEBUG')



    # File upload path
    MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'static/uploads')
