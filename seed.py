"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    #generate data from file
    for row in open('seed_data/u.item'):
        row = row.rstrip()
        row = row.split("|")

        #to get rid of (year), we could use regex...but we're not
        movie_id = int(row[0])
        title = row[1][:-7]

        #clean up date, create datetime object
        date_string = row[2]  #as string format (##-mon-####)

        if date_string:
            released_at = datetime.strptime(date_string, '%d-%b-%Y') #as datetime object
        else:
            released_at = None #is it a datetime object?

        imdb_url = row[4]

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(movie)

    #add to database
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    for row in open('seed_data/u.data'):
        row = row.rstrip()
        user_id, movie_id, score, not_using_this = row.split('\t')

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
