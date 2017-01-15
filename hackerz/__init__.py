from flask import Flask, g

# Initialize flask
app = Flask(__name__, instance_relative_config=True)


# Load default configuration
from .config import DefaultConfig
app.config.from_object(DefaultConfig)

# Load instance configuration
import os
CONFIG_ENVVAR = 'HACKERZ_CONFIG'
config_env = os.getenv(CONFIG_ENVVAR)
if config_env is not None:
    try:
        app.config.from_pyfile(config_env)
    except Exception:
        logging.exception('%s is not set correctly' % CONFIG_ENVVAR)


# Initialize SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_oauthlib.client import OAuth
oauth = OAuth()


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

from geopy.geocoders import Nominatim
gc = Nominatim().geocode

# Import home page
from .home import home
app.register_blueprint(home)

# Import error pages
from .errors import errors
app.register_blueprint(errors)

# Initialize navbar
from .nav import nav
nav.init_app(app)


# Initialize db
db.create_all()

