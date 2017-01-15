from flask import (Blueprint,
                   render_template, redirect,
                   request, session, url_for)
from . import app, db, oauth


spotify = Blueprint('spotify', __name__)

sp = oauth.remote_app('spotify',
    base_url='https://api.spotify.com/v1/',
    request_token_url=None,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
    consumer_key=app.config['SP_APP_ID'],
    consumer_secret=app.config['SP_APP_SECRET'],
    request_token_params={'scope': ('user-follow-read user-top-read user-read-email user-read-private')}
)

@sp.tokengetter
def get_spotify_token():
    return session.get('spotify_token')

def pop_spotify_session():
    session.pop('spotify_logged_in', None)
    session.pop('spotify_token', None)

@spotify.route("/spotify_login")
def spotify_login():
    return sp.authorize(callback=url_for('.spotify_authorized',
        next=request.args.get('next'), _external=True))

@spotify.route("/spotify_authorized")
@sp.authorized_handler
def spotify_authorized(resp):
    next_url = request.args.get('next') or url_for('home.index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['spotify_logged_in'] = True
    session['spotify_token'] = (resp['access_token'], '')

    return redirect(next_url)
