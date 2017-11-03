"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                           self.email)


# Put your Movie and Rating model classes here.
class Movie(db.Model):
    """Movie being rated"""

    __tablename__ = "movies"
    #the seed data has id on it already; will incriment fuck up
    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie title=%s>" % (self.title)


class Rating(db.Model):
    """Rating of movie by user"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   #define movie_id and user_id as foreign keys from the Primary keys of 
   #Movie and User
    movie_id = db.Column(db.Integer,
                         db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # Define relationship to user (self.user = User object)
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        
        return "<Rating score=%s>" % (self.score)



#############################################################
# Making some model data for our tests



##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///ratings'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    #default db_uri provided so tests can use other db
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
