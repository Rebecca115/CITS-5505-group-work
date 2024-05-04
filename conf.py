import os

class Config(object):
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Secret key for signing cookies
    SECRET_KEY = 'abcdsacb12312'

    # Mail configuration
    MAIL_SERVER = 'email-smtp.ap-southeast-2.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USERNAME = 'AKIAQOOWVOHOVKKRGKV7'
    MAIL_PASSWORD = 'BJMOOGNoMb/rBnzpS9qUX+VfO0K+W3AYDcvKq/gym9pb'
    MAIL_DEFAULT_SENDER = 'hello@fudongs.com'

    # File upload path
    MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'static/uploads')
