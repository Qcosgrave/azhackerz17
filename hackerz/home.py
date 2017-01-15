from facebook import get_user_from_cookie, GraphAPI
from flask import (Blueprint, current_app,
                   g, render_template, redirect,
                   request, session, url_for)
from flask_nav.elements import Navbar, View, Link


home = Blueprint('home', __name__)

from .nav import nav
navbar = Navbar('hackerz',
                View('Home', '.index'))
nav.register_element('site_nav', navbar)

from . import db

@home.route('/')
def index():
    FB_APP_NAME = current_app.config['FB_APP_NAME']
    FB_APP_ID= current_app.config['FB_APP_ID']
    if g.user:
        return render_template('index.html',
                               title=FB_APP_NAME,
                               app_id=FB_APP_ID,
                               user=g.user)
    return render_template('login.html',
                           title=FB_APP_NAME,
                           app_id=FB_APP_ID)

@home.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@home.before_request
def get_current_user():
    """Set g.user to the currently logged in user.
    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.
    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    FB_APP_ID= current_app.config['FB_APP_ID']
    FB_APP_SECRET = current_app.config['FB_APP_SECRET']

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get('user'):
        g.user = session.get('user')
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)

    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.
        user = User.query.filter(User.id == result['uid']).first()

        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me')
            if 'link' not in profile:
                profile['link'] = ""

            if 'location' in profile:
                location_name = profile['location']['name']
            else:
                location_name = None

            # Create the user and insert it into the database
            user = User(id=str(profile['id']), name=profile['name'],
                        profile_url=profile['link'],
                        access_token=result['access_token'],
                        email=profile['email'], location_name=location_name)
            db.session.add(user)
        elif user.access_token != result['access_token']:
            # If an existing user, update the access token
            user.access_token = result['access_token']

        # Add the user to the current session
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token,
                               email=user.email, location_name=user.location_name)

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get('user', None)
