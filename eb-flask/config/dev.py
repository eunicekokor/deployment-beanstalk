from os import path, pardir
from sys import stderr, exit


try:
    import secrets

    # Secret Values
    CSRF_SESSION_KEY = secrets.CSRF_SESSION_KEY
    SECRET_KEY = secrets.SECRET_KEY
    STRIPE_SECRET_KEY = secrets.STRIPE_TEST_SECRET_KEY
    STRIPE_PUBLISHABLE_KEY = secrets.STRIPE_TEST_PUBLISHABLE_KEY
    AWS_ACCESS_KEY_ID = secrets.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = secrets.AWS_SECRET_ACCESS_KEY

    # Flask configurations
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True

    # JWT
    JWT_TOKEN_LOCATION = ['cookies']

    # Meta
    META_TITLE = ''
    META_DESCRIPTION = ''
    META_DOMAIN = ''
    SSL = False
    META_URL = ('https://' if SSL else 'http://') + META_DOMAIN

    # SCSS Options
    SCSS_CONFIG_FILE = 'config/scss.json'

    # Base directory
    BASEDIR = path.abspath(path.join(path.dirname(__file__), pardir))

    # Cross-site request forgery configurations
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True

    # Logging configurations
    LOG_FILE_MAX_SIZE = '256'
    APP_LOG_NAME = 'app.log'
    WERKZEUG_LOG_NAME = 'werkzeug.log'

except ImportError:
    print >> stderr, ('Failed to import config/secrets.py.')
    exit(1)
