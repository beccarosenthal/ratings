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


@app.route('/register')
def register_form():

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_form():

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
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    #get form data
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    user_object = User.query.filter(User.email == user_email).first()
    if user_object:
    # if user_email in db.session.query(User.email).all():
        print "in the database"
        
        if user_object.password == user_password:
            flash("You're logged in. Welcome to Ratingsville! ~rate away~")
            session['current_user'] = user_email
            return redirect('/')

        else:
            flash("That is an incorrect password")
            return redirect('/login')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
