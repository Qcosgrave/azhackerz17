import logging
logger = logging.getLogger(__name__)


from flask import Flask

# Initialize flask
app = Flask(__name__)


# Load default configuration
from .config import DefaultConfig
app.config.from_object(DefaultConfig)

# Load instance configuration
import os
CONFIG_ENVVAR = 'HACKERZ_CONFIG'
config_env = os.getenv(CONFIG_ENVVAR)
if config_env is not None:
    try:
        config.from_pyfile(config_env)
    except Exception:
        logging.exception('%s is not set correctly' % CONFIG_ENVVAR)


# Initialize SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


# Initialize Flask-Bootstrap
from flask_bootstrap import Bootstrap, WebCDN
Bootstrap(app)

# Set up various js and css library CDNs
app.extensions['bootstrap']['cdns'] = {
        'bootstrap': WebCDN(
            '//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/'),
        'jquery': WebCDN(
            '//cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/'),
        'html5shiv': WebCDN(
            '//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/'),
        'respond.js': WebCDN(
            '//cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/')
}


# Import home page
from .home import home, navbar
app.register_blueprint(home)

# Import error pages
from .errors import errors
app.register_blueprint(errors)


# Initialize navbar
from .nav import nav
nav.init_app(app)


# Initialize db
db.create_all()
