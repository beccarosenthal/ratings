"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension




app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""


    return render_template('/homepage.html')


@app.route('/users')
def display_users():
    """lists users with email addresses and user ids)"""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<specific_user_id>')
def show_specific_user(specific_user_id):

    specific_user = User.query.filter(User.user_id == specific_user_id).one()
    print specific_user
    return render_template('user.html', user=specific_user)
    

@app.route('/register')
def register_form():
    """show registration form"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_form():
    """process registration form"""
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    user_object = User.query.filter(User.email == user_email).first()
    if user_object:

        flash("You already have an account. Please log in!")
        return redirect('/login')
    #If user object with email address provided doens't exist, add to db...
    else:        
        new_user = User(email=user_email,
                        password=user_password,
                        age=age,
                        zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/login')


@app.route('/login')
def show_login_form():
    """render login form"""

    if 'current_user' in session:
        flash('You\'re already logged in...silly goose')
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """process login form, redirect to user's page when it works"""
    #get form data
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    user_object = User.query.filter(User.email == user_email).first()
    if user_object:        

        if user_object.password == user_password:
            flash("You're logged in. Welcome to Ratingsville! ~rate away~")
            specific_user_id = user_object.user_id
            session['current_user'] = specific_user_id

            #What is the specific user ID
            url = '/users/' + str(specific_user_id)
            return redirect(url)

        else:
            flash("That is an incorrect password")
            return redirect('/login')
    else:
        flash('You need to register first!')
        return redirect('/register')


@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    del session['current_user']
    flash('successfully logged out...50-50 odds')
    return redirect ('/')


@app.route('/movies')
def show_all_movies():
    """Displays list of all movies"""

    movies = Movie.query.order_by(Movie.title).all()

    return render_template('movie_list.html', movies=movies)


@app.route('/movies/<specific_movie_id>')
def show_specific_movie(specific_movie_id):
    """show movie details page for specific movie by id"""

    specific_movie = Movie.query.filter(Movie.movie_id ==
                                        specific_movie_id).one()
    
    #getting average score to pass into jinja
    total_score = 0
    for rating_obj in specific_movie.ratings:
        total_score +=rating_obj.score
    
    avg = float(total_score) / len(specific_movie.ratings)

    user_has_rated = False

    if 'current_user' in session:
    #figure out if logged in user has already rated that movie
        for rating_obj in specific_movie.ratings:
            if rating_obj.user_id == session['current_user']:
                user_has_rated = True
                break

    return render_template('movie.html', movie=specific_movie,
                            user_has_rated=user_has_rated,
                            avg=avg)


@app.route('/add_rating')
def add_user_rating():
    """take user rating for movie, add to db"""


    user_id = int(session['current_user'])
    movie_id = int(request.args.get('movie_id'))
    new_rating = int(request.args.get('user_rating'))
    
    current_rating = Rating.query.filter(Rating.movie_id == movie_id,
                                         Rating.user_id == user_id).first()
    if not current_rating:
        rating_to_add = Rating(score=new_rating,
                               user_id=user_id, 
                               movie_id=movie_id)

        db.session.add(rating_to_add)

    else:
        current_rating.score = new_rating
        
    db.session.commit()

    return redirect('/movies/' + str(movie_id))
   

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
