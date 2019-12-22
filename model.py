from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import dateutil
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()




class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='Venue',cascade="all,delete", lazy=True)

    def __repr__(self):
        return f'<{self.id} {self.name}>'

    @property
    def past_shows(self):
        current_time = datetime.now()
        baseQuery = db.session.query(Show).filter(Show.start_time <= current_time)
        query_past_shows = baseQuery.filter_by(venue_id=self.id).all()
        past_shows_count = baseQuery.filter_by(venue_id=self.id).count()
        all_events = db.session.query(Show)
        return {"past_shows": query_past_shows,
                "past_shows_count": past_shows_count,
                }

    @property
    def upcoming_shows(self):
        current_time = datetime.now()
        baseQuery = db.session.query(Show).filter(Show.start_time >= current_time)
        query_upcoming_shows = baseQuery.filter_by(venue_id=self.id).all()
        upcoming_shows_count = baseQuery.filter_by(venue_id=self.id).count()
        return {"upcoming_shows": query_upcoming_shows,
                "upcoming_shows_count": upcoming_shows_count
                }

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), default=False)
    shows = db.relationship('Show', backref='Artist', lazy=True, )

    def __repr__(self):
        return f'<{self.id} {self.name}>'

    @property
    def past_shows(self):
        current_time = datetime.now()
        baseQuery = db.session.query(Show).filter(Show.start_time <= current_time)
        query_past_shows = baseQuery.filter_by(artist_id=self.id).all()
        past_shows_count = baseQuery.filter_by(artist_id=self.id).count()
        return {"past_shows": query_past_shows,
                "past_shows_count": past_shows_count,
                }
    @property
    def upcoming_shows(self):
        current_time = datetime.now()
        baseQuery = db.session.query(Show).filter(Show.start_time >= current_time)
        query_upcoming_shows = baseQuery.filter_by(artist_id=self.id).all()
        upcoming_shows_count = baseQuery.filter_by(artist_id=self.id).count()
        return {"upcoming_shows": query_upcoming_shows,
                "upcoming_shows_count": upcoming_shows_count
                }

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
    start_time = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<artist_id: {self.artist_id} venue_id: {self.venue_id}>'


