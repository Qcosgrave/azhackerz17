from flask import (Blueprint,
                   render_template, redirect,
                   request, session, url_for)
from flask_oauthlib.client import OAuth
from . import app, db, oauth


facebook = Blueprint('facebook', __name__)

fb = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/v2.8/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FB_APP_ID'],
    consumer_secret=app.config['FB_APP_SECRET'],
    request_token_params={'scope': ('email, ')}
)

@fb.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_facebook_session():
    session.pop('facebook_logged_in', None)
    session.pop('facebook_token', None)

@facebook.route("/facebook_login")
def facebook_login():
    return fb.authorize(callback=url_for('.facebook_authorized',
        next=request.args.get('next'), _external=True))

@facebook.route("/facebook_authorized")
@fb.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home.index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['facebook_logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)
