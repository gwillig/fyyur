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
from model import *
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
    db.session.commit()
########### Create data if empty
def load_data():
    def delete_all():
        db.session.rollback()
        db.session.query(Show).delete()
        db.session.query(Venue).delete()
        db.session.query(Artist).delete()
        db.session.commit()

    if db.session.query(Venue).count()!= 0:
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
        "genres": "Rock n Roll",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "website": "https://www.gunsnpetalsband.com",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"
    }
    artist2 = {
        "name": "Matt Quevedo",
        "genres": "Jazz",
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    }
    artist3 = {
        "name": "The Wild Sax Band",
        "genres": "Jazz,Classical",
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
        "venue_id": db.session.query(Venue).filter_by(name="The Musical Hop").first().id,
        "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2019-05-21T21:30:00.000Z")
    }, {
        "venue_id":  db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id":  db.session.query(Artist).filter_by(name="Matt Quevedo").first().id,
        "start_time": dateutil.parser.parse("2019-06-15T23:00:00.000Z")
    }, {
        "venue_id":  db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id":db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2035-04-01T20:00:00.000Z")
    }, {
        "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
        "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
        "start_time": dateutil.parser.parse("2035-04-08T20:00:00.000Z")
    },
        {
            "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
            "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
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
#####################
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
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
    for upcoming_show in venue.upcoming_shows["upcoming_shows"]:
        venue_dict["upcoming_shows"].append(
            {
                "start_time": upcoming_show.start_time,
                "artist_id": upcoming_show.Artist.id,
                "artist_name": upcoming_show.Artist.name,
                "artist_image_link": upcoming_show.Artist.image_link,
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
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Done: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    try:
        venue_name = db.session.query(Venue).filter_by(id=venue_id).first().name
        db.session.query(Venue).filter_by(id=venue_id).delete()
        db.session.commit()
        print(f'{venue_name} was successfully deleted')
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()


    return redirect(url_for('venues'))

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
    # Done: replace with real venue data from the venues table, using venue_id
    try:
       artist = db.session.query(Artist).filter_by(id=artist_id).first()
       artist_dict = artist.__dict__
       artist_dict["past_shows"] = []
       artist_dict["upcoming_shows"] = []
       artist_dict["past_shows_count"] = artist.past_shows['past_shows_count']
       artist_dict["upcoming_shows_count"] = artist.upcoming_shows['upcoming_shows_count']
       artist_dict["genres"] = artist_dict["genres"].split(",")

       # Get all the past_shows
       for past_show in artist.past_shows["past_shows"]:
           artist_dict["past_shows"].append(
               {
                   "start_time": past_show.start_time,
                   "artist_id": past_show.Artist.id,
                   "artist_name": past_show.Artist.name,
                   "artist_image_link": past_show.Artist.image_link,
               }
           )
       for upcoming_shows in artist.upcoming_shows["upcoming_shows"]:
           artist_dict["upcoming_shows"].append(
               {
                   "start_time": upcoming_shows.start_time,
                   "artist_id": upcoming_shows.Artist.id,
                   "artist_name": upcoming_shows.Artist.name,
                   "artist_image_link": upcoming_shows.Artist.image_link,
               }
           )

    except:
        db.session.rollback()
        print(sys.exc_info())
        artist_dict = {
            "id": 4,
            "name": "Error occur. Please contact admin",
            "genres": [],
            "city": "",
            "state": "",
            "phone": "",
            "website": "",
            "facebook_link": "",
            "seeking_venue": True,
            "seeking_description": "",
            "image_link": "",
            "past_shows": [],
            "upcoming_shows": [],
            "past_shows_count": 0,
            "upcoming_shows_count": 0,
        }
    finally:
        db.session.close()

    return render_template('pages/show_artist.html', artist=artist_dict)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    artist = db.session.query(Artist).filter_by(id=artist_id).first()
    form = ArtistForm()
    form.name.data = artist.name
    form.image_link.data = artist.image_link
    form.phone.data = artist.phone
    form.state.data = artist.state
    form.city.data = artist.city
    form.facebook_link.data = artist.facebook_link
    form.genres.data = artist.genres.split(",")

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    try:
        form = ArtistForm(request.form)
        artist = db.session.query(Artist).filter_by(id=artist_id).first()
        artist.name = form.name.data
        artist.name = form.name.data
        artist.image_link = form.image_link.data
        artist.phone = form.phone.data
        artist.state = form.state.data
        artist.city = form.city.data
        artist.facebook_link = form.facebook_link.data
        artist.genres = ",".join(form.genres.data)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.close()
        return render_template('errors/404.html'), 404
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    form.name.data = venue.name
    form.image_link.data = venue.image_link
    form.phone.data = venue.phone
    form.state.data = venue.state
    form.city.data = venue.city
    form.address.data = venue.address
    form.facebook_link.data = venue.facebook_link
    form.genres.data = venue.genres.split(",")
    venue_dict = venue.__dict__
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

    return render_template('forms/edit_venue.html', form=form, venue=venue_dict)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Done: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        form = VenueForm(request.form)
        venue = db.session.query(Venue).filter_by(id=venue_id).first()
        venue.name = form.name.data
        venue.name = form.name.data
        venue.image_link = form.image_link.data
        venue.phone = form.phone.data
        venue.state = form.state.data
        venue.city = form.city.data
        venue.facebook_link = form.facebook_link.data
        venue.genres = ",".join(form.genres.data)
        venue.address = form.address.data
        db.session.commit()
    except:
        db.session.rollback()
        db.session.close()
        return render_template('errors/404.html'), 404
    finally:
        db.session.close()

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
    try:
        form = ArtistForm(request.form)
        artist = Artist()
        artist.name = form.name.data
        artist.name = form.name.data
        artist.image_link = form.image_link.data
        artist.phone = form.phone.data
        artist.state = form.state.data
        artist.city = form.city.data
        artist.facebook_link = form.facebook_link.data
        artist.genres = ",".join(form.genres.data)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        db.session.close()
        flash('Error occur! Artist ' + request.form['name'] + ' was not successfully listed!')
    finally:
        db.session.close()

    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')

    # on successful db insert, flash success





#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    all_shows = db.session.query(Show).all()
    data = []
    for show in all_shows:
        data.append(
            {
            "venue_id": show.venue_id,
            "venue_name": show.Venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.start_time
            }
        )

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        new_show = {
            "artist_id": request.form['artist_id'],
            "venue_id": request.form['venue_id'],
            "start_time": request.form['start_time'],

        }
        s1 = Show(**new_show)
        db.session.add(s1)
        db.session.commit()
        flash('Show at ' + request.form['start_time'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Show at ' + request.form['start_time'] + ' could not be listed.')
    finally:
        db.session.close()

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
