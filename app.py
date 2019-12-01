# ----------------------------------------------------------------------------#
# Own Notes.
"""
Description                         | Cmd
to login as the right user for psql | PGUSER=test PGPASSWORD=test psql -h localhost test
Give all right to role              | GRANT ALL PRIVILEGES ON database test to test;
adds temporary git\bit to path      | "c:\Program Files\Git\bin\sh.exe" --login

PGUSER=test PGPASSWORD=test psql -h localhost todoapp
"""
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import dateutil.parser
import sys
from datetime import datetime
import json
from sqlalchemy import func
import dateutil.parser
from sqlalchemy import distinct
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ------------------------------------------
# import psycopg2
# conn = psycopg2.connect( 'postgresql://test:test@localhost:15432/test')
# cur = conn.cursor()
# cur.execute("Select city,count(city) from Venue GROUP BY city;")
# print(cur.fetchall())
# result = cur.fetchall()
# conn.rollback()
# Models.
# ----------------------------------------------------------------------------#

db.metadata.clear()


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
    show = db.relationship('Show', backref='Venue', lazy=True)

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


db.create_all()


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
    start_time = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<artist_id: {self.artist_id} venue_id: {self.venue_id}>'


db.create_all()
db.session.commit()


########### Create data if empty
def load_data():
    def delete_all():
        db.session.rollback()
        Show.query.delete()
        Venue.query.delete()
        Artist.query.delete()
        db.session.commit()

    if Venue.query.count() != 0:
        print("Deleted old records")
        delete_all()

    venue1 = {
        "name": "The Musical Hop",
        "city": "San Francisco",
        "state": "CA",
        "address": "1015 Folsom Street",
        "phone": "123-123-1234",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "website": "https://www.themusicalhop.com",
        "genres": 'Jazz,Reggae,Swing,Classical,Folk',
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us."
    }
    venue2 = {
        "name": "The Dueling Pianos Bar",
        "genres": 'Classical, R&B, Hip-Hop',
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    }
    venue3 = {
        "name": "Park Square Live Music & Coffee",
        "genres": 'Rock n Roll, Jazz, Classical, Folk',
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    }

    v1 = Venue(**venue1)
    v2 = Venue(**venue2)
    v3 = Venue(**venue3)
    db.session.add_all([v1, v2, v3])
    db.session.commit()
    ###################################
    artist1 = {
        "name": "Guns N Petals",
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "genres": ["Rock n Roll"],
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "website": "https://www.gunsnpetalsband.com",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"
    }
    artist2 = {
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    }
    artist3 = {
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    }
    a1 = Artist(**artist1)
    a2 = Artist(**artist2)
    a3 = Artist(**artist3)
    db.session.add_all([a1, a2, a3])
    db.session.commit()
    ####################################### Show data

    data = [{
        "venue_id": Venue.query.filter_by(name="The Musical Hop").first().id,
        "artist_id": Artist.query.filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2019-05-21T21:30:00.000Z")
    }, {
        "venue_id": Venue.query.filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id": Artist.query.filter_by(name="Matt Quevedo").first().id,
        "start_time": dateutil.parser.parse("2019-06-15T23:00:00.000Z")
    }, {
        "venue_id": Venue.query.filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id": Artist.query.filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2035-04-01T20:00:00.000Z")
    }, {
        "venue_id": Venue.query.filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id": Artist.query.filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2035-04-08T20:00:00.000Z")
    },
        {
            "venue_id": Venue.query.filter_by(name="Park Square Live Music & Coffee").first().id,
            "artist_id": Artist.query.filter_by(name="The Wild Sax Band").first().id,
            "start_time": dateutil.parser.parse("2035-04-15T20:00:00.000Z")
        }
    ]
    s_list = [Show(**x) for x in data]
    # sh1 = data[0]
    # db.session.add(Show(**sh1))
    db.session.commit()
    db.session.add_all(s_list)
    db.session.commit()

load_data()
#####################
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  print("hello")
  if type(value)!=str:
    date=value
  else:
    date = dateutil.parser.parse(value)
  if format == 'full':
      format = "%Y-%m-%d  at %H:%M"
  elif format == 'medium':
      format = "%Y-%m-%d  at %H:%M"
  return date.strftime(format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    db.session.rollback()
    db.metadata.clear()
    city_state = db.session.query(Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()

    result = []
    '1.Step: Filter for each location to get the venues'
    for v in city_state:
        v_result = {"city": v.city, "state": v.state, "venues": []}
        venues_of_v = db.session.query(Venue.name, Venue.id).filter_by(city=v.city, state=v.state).all()
        print(venues_of_v)
        for single_venue in venues_of_v:
            venue_dict = {}
            venue_dict["id"] = single_venue[1]
            venue_dict["name"] = single_venue[0]
            venue_dict["num_upcoming_shows"] = \
            db.session.query(Venue).filter_by(id=single_venue[1]).first().upcoming_shows["upcoming_shows_count"]
            v_result["venues"].append(venue_dict)
        result.append(v_result)

    return render_template('pages/venues.html', areas=result);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form['search_term']
    baseQuery = db.session.query(Venue).filter(Venue.name.like(f'%{search_term}%'))
    response = {
      "data": [],
      "count": baseQuery.count()
    }
    search_result = baseQuery.all()
    for el in search_result:
        response["data"].append(
            {
                "id": el.id,
                "name": el.name,
                "num_upcoming_shows": el.upcoming_shows['num'],
            }
        )
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # print(request.data)
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    venue_dict = venue.__dict__
    venue_dict["genres"] = venue_dict["genres"].split(",")
    venue_dict["past_shows"]=[]
    #Get all the artist from past_shows
    for past_show in venue.past_shows["past_shows"]:
        venue_dict["past_shows"].append(
            {
              "start_time":past_show.start_time,
              "artist_id": past_show.Artist.id,
              "artist_name": past_show.Artist.name,
              "artist_image_link": past_show.Artist.image_link,
            }
        )

    return render_template('pages/show_venue.html', venue=venue_dict)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # Done: insert form data as a new Venue record in the db, instead
    # Done: modify data to be the data object returned from db insertion
    try:
        new_venue= {
            "name": request.form['name'],
            "city": request.form['city'],
            "state": request.form['state'],
            "address": request.form['address'],
            "phone":  request.form['phone'],
            "facebook_link": request.form['facebook_link'],
            "genres": request.form['genres'],
        }
        v1 = Venue(**new_venue)
        db.session.add(v1)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # Done: replace with real data returned from querying the database
    data = []
    try:

        all_artists = db.session.query(Artist.id,Artist.name).all()
        for ar in all_artists:
            data.append(
                {
                    "id":ar.id,
                    'name':ar.name
                }
            )
    except:
        data.append({
        "id": 4,
        "name": "Error occur. Please contact the admin",
        })
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevedo", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
###############################
    search_term = request.form['search_term']
    baseQuery = db.session.query(Artist).filter(Artist.name.like(f'%{search_term}%'))
    if baseQuery.count()!=0:
        response = {
            "count": baseQuery.count(),
            "data": [{
                "id": baseQuery.first().id,
                "name": baseQuery.first().name,
                "num_upcoming_shows": baseQuery.first().upcoming_shows["upcoming_shows_count"],
            }]
        }
    else:
        #if search was not successfull
        response = {
            "count": 0,
            "data": [{
                "id": 0,
                "name": "No hit",
                "num_upcoming_shows": 0,
            }]
        }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data1 = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 5,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }
    ]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
