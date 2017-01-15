from datetime import datetime

from app import db


class SPUser(db.Model):
    __tablename__ = 'spusers'
    pass

class FBUser(db.Model):
    __tablename__ = 'fbusers'

    id = db.Column(db.String, nullable=False, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    # Check if user has not set location and give a warning, but could be empty
    location_name = db.Column(db.String, nullable=True)

