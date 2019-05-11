#!/usr/bin/env python

"""application.py: 'OTR Program Catalog' RESTful web application.

'OTR Program Catalog' is a Flask web application with a SQLite back end
that provides an interface for browsing and managing a catalog of Old
Time Radio (OTR) genres and programs. It is written in Python 2 and
leverages Google oauth for user login.

Usage:
    python application.py

For additional information, please see the README file.
"""

from models import Base, User, Genre, Program
from flask import (Flask, jsonify, request, redirect, url_for, abort, g,
                   render_template, flash, make_response,
                   session as login_session)
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from sqlalchemy import create_engine, event

import httplib2
import requests
import json
import sys
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


# Function to enforce foreign keys for SQLite (triggered by 'connect' event
# handler below). Taken from users 'conny' and 'CarlS' on StackOverflow
# (https://stackoverflow.com/questions/2614984/ ...
# sqlite-sqlalchemy-how-to-enforce-foreign-keys/7831210#7831210)
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


# Connect to Database and create database session.
engine = create_engine('sqlite:///otrCatalog.db',
                       connect_args={'check_same_thread': False})
event.listen(engine, 'connect', _fk_pragma_on_connect)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# Retrieve client id from client_secrets file.
CLIENT_ID = json.loads(
                       open('client_secrets.json', 'r').read()
                      )['web']['client_id']


# ENDPOINTS
@app.route('/')
def latestPrograms():
    """Show application home page.

    Returns:
        Page displaying 10 most recently added programs.
    """
    genres = session.query(Genre).order_by('name').all()
    latest_progs = session.query(
                                 Program.id, Program.genre_id,
                                 Program.time_created, Program.name,
                                 Genre.name
                                ).join(
                                       Genre, Program.genre_id == Genre.id
                                      ).order_by(
                                                 Program.time_created.desc()
                                                ).limit(10)
    return render_template('latestPrograms.html', genres=genres,
                           latest_progs=latest_progs)


@app.route('/genre/add', methods=['GET', 'POST'])
def addGenre():
    """Add a new genre to the database.

    Returns:
        If user is not signed in, redirect to login page.
        on GET: Page with form to add a new genre.
        on POST: Redirect to page showing new genre after it's created.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        return render_template('addGenre.html', genres=genres)
    elif request.method == 'POST':
        name = request.form.get('name')
        user_id = login_session['user_id']

        numThisGenre = session.query(Genre).filter_by(name=name).count()
        if numThisGenre > 0:
            flash('The genre you attempted to add already exists.')
            return redirect(request.path)

        genre = Genre(name=name, user_id=user_id)
        session.add(genre)
        session.commit()
        flash("Genre \"%s\" created." % name)
        return redirect(url_for('showGenre', genre_id=genre.id))


@app.route('/genre/<int:genre_id>')
@app.route('/genre/<int:genre_id>/program')
def showGenre(genre_id):
    """Show all programs within the specified genre.

    Args:
        genre_id (int): Primary key of specified genre.

    Returns:
        Page showing specified genre and all programs within it.
    """
    genres = session.query(Genre).order_by('name').all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    programs = session.query(Program).filter_by(
                                                genre_id=genre_id
                                               ).order_by('name').all()
    return render_template('showGenre.html', genres=genres, genre=genre,
                           programs=programs)


@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    """Delete specified genre from database.

    Args:
        genre_id (int): Primary key of specified genre.

    Returns:
        If user is not signed in, redirect to login page.
        If logged-in user did not create the genre, redirect to page
            showing genre and flash error message.
        If genre has programs associated with it, redirect to page
            showing genre and flash error message.
        on GET: Page with form confirming intent to delete.
        on POST: Redirect to application home page after deletion.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if genre.user_id != login_session['user_id']:
        flash('You may not delete a genre which you did not create.')
        return redirect("/genre/%s" % genre_id)
    numPrograms = session.query(Program).filter_by(
                                                   genre_id=genre_id
                                                  ).count()
    if numPrograms > 0:
        flash('You may not delete a genre which contains programs.')
        return redirect("/genre/%s" % genre_id)
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        return render_template('deleteGenre.html', genres=genres, genre=genre)
    elif request.method == 'POST':
        session.delete(genre)
        session.commit()
        flash("Genre \"%s\" deleted." % genre.name)
        return redirect(url_for('latestPrograms'))


@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def editGenre(genre_id):
    """Edit specified genre.

    Args:
        genre_id (int): Primary key of specified genre.

    Returns:
        If user is not signed in, redirect to login page.
        If logged-in user did not create the genre, redirect to page
            showing genre and flash error message.
        on GET: Page with form for user to specify desired edits.
        on POST: Redirect to application home page after edits.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if genre.user_id != login_session['user_id']:
        flash('You may not edit a genre which you did not create.')
        return redirect(request.path)
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        return render_template('editGenre.html', genres=genres, genre=genre)
    elif request.method == 'POST':
        name = request.form.get('name')
        genre.name = name
        session.commit()
        flash("Genre \"%s\" updated." % genre.name)
        return redirect(url_for('latestPrograms'))


@app.route('/genre/<int:genre_id>/program/add', methods=['GET', 'POST'])
def addProgram(genre_id):
    """Add a program to specified genre.

    Args:
        genre_id (int): Primary key of specified genre.

    Returns:
        If user is not signed in, redirect to login page.
        on GET: Page with form for user to submit new program details.
        on POST: Redirect to read-only page showing program details.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        genre = session.query(Genre).filter_by(id=genre_id).one()
        return render_template('addProgram.html', genres=genres, genre=genre)
    elif request.method == 'POST':
        name = request.form.get('name')
        yearBegan = request.form.get('yearBegan')
        yearEnded = request.form.get('yearEnded')
        description = request.form.get('description')
        user_id = login_session['user_id']

        numPrograms = session.query(Program).filter_by(genre_id=genre_id,
                                                       name=name).count()
        if numPrograms > 0:
            flash('The program you are attempting to add already exists.')
            return redirect(request.path)
        program = Program(name=name, yearBegan=yearBegan, yearEnded=yearEnded,
                          description=description, genre_id=genre_id,
                          user_id=user_id)
        session.add(program)
        session.commit()
        flash("Program \"%s\" created." % program.name)
        return redirect(url_for('showProgram', genre_id=genre_id,
                                program_id=program.id))


@app.route('/genre/<int:genre_id>/program/<int:program_id>/edit',
           methods=['GET', 'POST'])
def editProgram(genre_id, program_id):
    """Edit details of specified program.

    Args:
        genre_id (int): Primary key of specified genre.
        program_id (int): Primary key of specified program.

    Returns:
        If user is not signed in, redirect to login page.
        If logged-in user did not create the program, redirect to page
            showing program and flash error message.
        on GET: Page with form for user to specify desired edits.
        on POST:
            If user is specifying a new program name which already
                exists within the genre, redirect to edit page and
                flash error message.
            Otherwise, redirect to read-only page showing program
                details.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    program = session.query(Program).filter_by(id=program_id).one()
    if program.user_id != login_session['user_id']:
        flash('You may not edit a program which you did not create.')
        return redirect(request.path)
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        return render_template('editProgram.html', genres=genres, genre=genre,
                               program=program)
    elif request.method == 'POST':
        name = request.form.get('name')
        yearBegan = request.form.get('yearBegan')
        yearEnded = request.form.get('yearEnded')
        description = request.form.get('description')

        numPrograms = session.query(Program).filter_by(genre_id=genre_id,
                                                       name=name).count()
        if numPrograms > 0 and name != program.name:
            flash('The program name you have entered already exists.')
            return redirect(request.path)
        program.name = name
        program.yearBegan = yearBegan
        program.yearEnded = yearEnded
        program.description = description

        session.commit()
        flash("Program \"%s\" updated." % program.name)
        return redirect(url_for('showProgram', genre_id=genre_id,
                                program_id=program_id))


@app.route('/genre/<int:genre_id>/program/<int:program_id>/delete',
           methods=['GET', 'POST'])
def deleteProgram(genre_id, program_id):
    """Delete specified program from database.

    Args:
        genre_id (int): Primary key of specified genre.
        program_id (int): Primary key of specified genre.

    Returns:
        If user is not signed in, redirect to login page.
        If logged-in user did not create the program, redirect to page
            showing program and flash error message.
        on GET: Page with form confirming intent to delete.
        on POST: Redirect to page showing genre with which deleted
            program was associated.
    """
    if 'user_name' not in login_session:
        login_session['target_path'] = request.path
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    program = session.query(Program).filter_by(id=program_id).one()
    if program.user_id != login_session['user_id']:
        flash('You may not delete a program which you did not create.')
        return redirect(request.path)
    if request.method == 'GET':
        genres = session.query(Genre).order_by('name').all()
        return render_template('deleteProgram.html', genres=genres,
                               genre=genre, program=program)
    elif request.method == 'POST':
        session.delete(program)
        session.commit()
        flash("Program \"%s\" deleted." % program.name)
        return redirect(url_for('showGenre', genre_id=genre_id))


@app.route('/genre/<int:genre_id>/program/<int:program_id>/show')
def showProgram(genre_id, program_id):
    """Show details of specified program.

    Args:
        genre_id (int): Primary key of specified genre.
        program_id (int): Primary key of specified program.

    Returns:
        Page showing program details.
    """
    genres = session.query(Genre).order_by('name').all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    program = session.query(Program).filter_by(id=program_id).one()
    return render_template('showProgram.html', genres=genres, genre=genre,
                           program=program)


@app.route('/login')
def login():
    """Return page presenting user with login option.

    Currently, Google login is the only option available.
    """
    # Add target_path to session (if applicable) to support redirecting to
    # user's intended destination after login is complete.
    if request.args.get('target_path') is not None:
        login_session['target_path'] = request.args.get('target_path')
    # Create anti-forgery state token; save in session and pass to html page.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Handle Ajax POST from Google sign-in callback in login.html.

    Validates state and header info and retrieves auth code from POST.
    Upgrades auth code to credentials object uses it to retrieve user
    information via Google API. Updates login session and database
    (User) table with information for logged-in user. Writes flash
    login success message on completion.

    Returns:
        If POSTed state token does not match one in session, 401 error.
        If request lacks `X-Requested-With` header, 403 error.
        If FlowExchangeError or other unspecified error encountered
            while exchanging auth code, 401 error.
        If error is encountered accessing user account info via
            access_token, 500 error.
        If unable to verify that access token is for the intended user,
            401 error.
        If unable to verify that access token is for the intended app,
            401 error.
        If access token corresponds to current logged-in session user,
            200 response.
        Otherwise, JSON string containing login success message (msg)
            and path (dest) representing intended post-login
            destination page, if any.
    """
    # Check that the state token from client matches the session version.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # (Receive auth_code from POST)
    auth_code = request.get_data()

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF.
    if not request.headers.get('X-Requested-With'):
        abort(403)

    try:
        # Upgrade the authorization code into a credentials object.
        print "Attempting to get credentials..."
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='',
                                             redirect_uri='postmessage')
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print e.message, e.args
        msg = "Unexpected error: %s" % e.message
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_user_id = credentials.id_token['sub']
    if result.get('user_id') != google_user_id:
        msg = "Token's user ID doesn't match given user ID."
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result.get('issued_to') != CLIENT_ID:
        msg = "Token's client ID does not match app's."
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_user_id = login_session.get('google_user_id')
    if stored_access_token is not None and google_user_id == stored_user_id:
        msg = 'Current user is already connected.'
        response = make_response(json.dumps(msg), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token and user id in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_user_id'] = google_user_id

    # Get user info from Google API.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    name = data['name']
    picture = data['picture']
    email = data['email']

    # Update user info in login_session.
    login_session['user_name'] = name
    login_session['picture'] = picture
    login_session['email'] = email

    # Add provider to login session.
    login_session['provider'] = 'google'

    # See if user exists in database; if not, make a new one.
    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(username=name, picture=picture, email=email)
        session.add(user)
    else:
        # Update name and picture using fresh data from Google.
        user.username = name
        user.picture = picture
    session.commit()
    login_session['user_id'] = user.id

    # Return message to client; also flash message
    msg = ''
    msg += '<h1>Welcome, '
    msg += login_session['user_name']

    msg += '!</h1>'
    msg += '<img src="'
    msg += login_session['picture']
    msg += ' " style="width:300px; height:300px;'
    msg += ' border-radius:150px;-webkit-border-radius:150px;'
    msg += ' -moz-border-radius:150px;"> '

    flash("Login successful.")

    dest = login_session.pop('target_path', None)
    return jsonify({'msg': msg, 'dest': dest})


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnect user logged-in with Google.

    Returns:
        If access token not in session, 401 error.
        If disconnect successful, 200 response.
        If disconnect unsuccessful, 400 error.
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # User is connected; attempt disconnect...
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        msg = 'Successfully disconnected.'
        response = make_response(json.dumps(msg), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        msg = 'Failed to revoke token for given user.'
        response = make_response(json.dumps(msg), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """Disconnect logged-in user and remove related session variables.

    Calls provider-specific disconnect function based on provider
    specified in login session. Adds flash message with logout status.

    Returns:
        Redirect to application home page.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            login_session.pop('access_token', None)
            login_session.pop('google_user_id', None)

        # Add disconnect code for other login providers here as needed...

        login_session.pop('user_id', None)
        login_session.pop('state', None)
        login_session.pop('user_name', None)
        login_session.pop('picture', None)
        login_session.pop('email', None)
        login_session.pop('provider', None)
        flash("You have been successfully logged out.")
    else:
        flash("You were not logged in.")

    # Return to home page.
    return redirect(url_for('latestPrograms'))


# JSON ENDPOINTS
@app.route('/genres/JSON')
def showGenresJSON():
    """Return JSON data representing all genres in the database."""
    genres = session.query(Genre).order_by('name').all()
    return jsonify(Genres=[i.serialize for i in genres])


@app.route('/genre/<int:genre_id>/programs/JSON')
def showGenreProgramsJSON(genre_id):
    """Return JSON data representing all programs in specified genre.

    Args:
        genre_id (int): Primary key of specified genre.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    programs = session.query(Program).filter_by(genre_id=genre_id
                                                ).order_by('name').all()
    return jsonify(Programs=[i.serialize for i in programs])


@app.route('/genre/<int:genre_id>/program/<int:program_id>/JSON')
def showProgramJSON(genre_id, program_id):
    """Return JSON data representing a specific program item.

    Args:
        genre_id (int): Primary key of specified genre.
        program_id (int): Primary key of specified program.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    program = session.query(Program).filter_by(genre_id=genre_id,
                                               id=program_id
                                               ).one()
    return jsonify(program.serialize)


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase +
                                       string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
