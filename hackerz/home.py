from facebook import get_user_from_cookie, GraphAPI
from flask import (Blueprint,
                   g, render_template, redirect,
                   request, session, url_for)
from flask_oauthlib.client import OAuth
from flask_nav.elements import Navbar, View, Link


home = Blueprint('home', __name__)

from .nav import nav
navbar = Navbar('hackerz',
                View('Home', '.index'))
nav.register_element('site_nav', navbar)

from . import app, db

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/v2.8/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FB_APP_ID'],
    consumer_secret=app.config['FB_APP_SECRET'],
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@home.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('.facebook_authorized',
        next=request.args.get('next'), _external=True))

@home.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('.index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@home.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('.index'))


@home.route('/')
def index():
    if session.get('logged_in', False):
        data = facebook.get('/me').data
    else:
        data={}
    return render_template('index.html', user=data)

