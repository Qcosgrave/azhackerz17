from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View, Link


home = Blueprint('home', __name__)

from .nav import nav
navbar = Navbar('site_nav',
                View('Home', '.index'))
nav.register_element('site_nav', navbar)

@home.route('/')
def index():
    return render_template('index.html')
