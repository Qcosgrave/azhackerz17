import json
import requests
from flask import (Blueprint,
                   render_template, redirect,
                   request, session, url_for)
from flask_nav.elements import Navbar, View, Link, RawTag, Text
from datetime import datetime, timedelta
from . import app, gc
from .facebook import facebook, fb, pop_facebook_session
from .spotify import spotify, sp, pop_spotify_session
from .nav import nav
from .util import fb_data, sp_data, fb_logged_in, sp_logged_in, find_airport, find_flight, find_events



home = Blueprint('home', __name__)

app.register_blueprint(facebook)
app.register_blueprint(spotify)

@nav.navigation('site_nav')
def navbar():
    fb_btn = Text('Logged in to Facebook')
    sp_btn = Text('Logged in to Spotify')
    signout = Text('')
    if not fb_logged_in():
        fb_btn = View('Log In To Facebook', 'facebook.facebook_login')
    else:
        fb_btn = Text('fb: ' + fb_data('')['name'])

    if not sp_logged_in():
        sp_btn = View('Log In To Spotify', 'spotify.spotify_login')
    else:
        sp_btn = Text('sp: ' + sp_data('')['email'])

    if fb_logged_in() or sp_logged_in():
        signout = View('Logout', '.logout')

    return Navbar('Spotiflyt',
                  View('Home', '.index'),
                  fb_btn, sp_btn, signout)
nav.register_element('site_nav', navbar)

@home.route("/logout")
def logout():
    pop_facebook_session()
    pop_spotify_session()
    return redirect(url_for('.index'))


@home.route('/')
def index():
    if fb_logged_in():
        loc = 'Tucson, AZ'
        #loc = fb_data('').get('location', {'name': ''})['name']
        lat_lon = gc(loc)
        lat, lon = (lat_lon.latitude, lat_lon.longitude) if lat_lon else (None, None)
        lat, lon = map(str, (lat, lon))

        try:
            airport = find_airport(lon, lat)
        except:
            airport = ''

        depart = datetime.now() + timedelta(days=6*30)

        event = "Chance the Rapper at the Blaisedell center"

        #events = find_events(['Drake'])

        flight = find_flight(airport, 'LAS', depart.strftime('%Y-%m-%d %H:%M:%S'), lat, lon)

    else:
        lat, lon = None, None
        loc = None
    return render_template('index.html',
                           fb_logged_in=fb_logged_in(),
                           loc=loc, lat=lat, lon=lon,
                           airport=airport, flight=flight,
                           event=event)

