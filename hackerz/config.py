class DefaultConfig(object):
    DEBUG = True

    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    THREADS_PER_PAGE = 2

    CSRF_ENABLED     = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = "secret"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    FB_APP_NAME = ''
    FB_APP_ID = ''
    FB_APP_SECRET = ''
